import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig } from "vitepress";

function excludeFromLocalSearch(relativePath: string): boolean {
  const normalized = relativePath.replace(/\\/g, "/");

  return (
    normalized.startsWith("plans/") ||
    normalized.startsWith("report/") ||
    // Keep local search focused on task-facing pages: landing, quick start,
    // usage, and skill overview pages. Long module/reference/resource pages
    // remain browsable through the sidebar but stay out of the generated index.
    normalized.includes("/resources/") ||
    normalized.includes("resources/")
  );
}

// ---------------------------------------------------------------------------
// Sidebar helpers
// ---------------------------------------------------------------------------

const P = "/skills";
const PZH = "/zh/skills";
const DOCS_DIR = fileURLToPath(new URL("..", import.meta.url));
const RESOURCE_KINDS = ["references", "templates", "examples", "agents"] as const;

type SidebarItem = {
  text: string;
  link?: string;
  collapsed?: boolean;
  items?: SidebarItem[];
};

const RESOURCE_LABELS = {
  en: {
    references: "References",
    templates: "Templates",
    examples: "Examples",
    agents: "Agent Contracts",
  },
  zh: {
    references: "参考资料",
    templates: "模板",
    examples: "示例",
    agents: "Agent 说明",
  },
};

const DIRECTORY_LABELS: Record<string, [string, string]> = {
  citations: ["Citations", "引用"],
  deai: ["DeAI", "去 AI"],
  evidence: ["Evidence", "证据"],
  formatting: ["Formatting", "格式"],
  latex: ["LaTeX", "LaTeX"],
  modules: ["Modules", "模块"],
  review: ["Review", "审阅"],
  "section-writing": ["Section Writing", "分节写作"],
  venues: ["Venues", "期刊与会议"],
  writing: ["Writing", "写作"],
};

function humanizeName(name: string): string {
  return name
    .replace(/\.md$/i, "")
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function readH1(file: string): string | undefined {
  const content = fs.readFileSync(file, "utf8");
  return content
    .split(/\r?\n/)
    .find((line) => /^#\s+/.test(line))
    ?.replace(/^#\s+/, "")
    .replace(/\s+#+\s*$/, "")
    .replace(/\`/g, "");
}

function directoryLabel(directory: string, isZh: boolean): string {
  const labels = DIRECTORY_LABELS[path.basename(directory).toLowerCase()];
  return labels ? labels[isZh ? 1 : 0] : humanizeName(path.basename(directory));
}

function directoryItems(
  directory: string,
  routeBase: string,
  isZh: boolean,
): SidebarItem[] {
  const entries = fs
    .readdirSync(directory, { withFileTypes: true })
    .filter((entry) => !entry.name.startsWith("."))
    .sort((left, right) => {
      if (left.isDirectory() !== right.isDirectory()) {
        return left.isDirectory() ? -1 : 1;
      }
      return left.name.localeCompare(right.name, "en", {
        sensitivity: "base",
      });
    });

  const items: SidebarItem[] = [];
  for (const entry of entries) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      const nested = directoryItems(
        absolute,
        `${routeBase}/${entry.name}`,
        isZh,
      );
      if (nested.length > 0) {
        const indexPath = path.join(absolute, "index.md");
        items.push({
          text: fs.existsSync(indexPath)
            ? readH1(indexPath) || directoryLabel(absolute, isZh)
            : directoryLabel(absolute, isZh),
          collapsed: true,
          items: nested,
        });
      }
      continue;
    }
    if (!entry.name.toLowerCase().endsWith(".md")) {
      continue;
    }
    const stem = entry.name.slice(0, -3);
    items.push({
      text: readH1(absolute) || humanizeName(entry.name),
      link:
        stem.toLowerCase() === "index"
          ? `${routeBase}/`
          : `${routeBase}/${stem}`,
    });
  }
  return items;
}

function resourceItems(prefix: string, skill: string): SidebarItem[] {
  const isZh = prefix.startsWith("/zh");
  const locale = isZh ? "zh" : "en";
  const skillDirectory = path.join(
    DOCS_DIR,
    ...(isZh ? ["zh"] : []),
    "skills",
    skill,
  );
  const resourceRoot = path.join(skillDirectory, "resources");
  if (!fs.existsSync(resourceRoot)) {
    return [];
  }

  const groups: SidebarItem[] = [];
  for (const kind of RESOURCE_KINDS) {
    const kindDirectory = path.join(resourceRoot, kind);
    if (!fs.existsSync(kindDirectory)) {
      continue;
    }
    const items = directoryItems(
      kindDirectory,
      `${prefix}/${skill}/resources/${kind}`,
      isZh,
    );
    if (items.length > 0) {
      groups.push({
        text: RESOURCE_LABELS[locale][kind],
        collapsed: true,
        items,
      });
    }
  }
  return groups;
}

function skillItems(prefix: string, skill: string): SidebarItem[] {
  const base = `${prefix}/${skill}`;
  const isZh = prefix.startsWith("/zh");
  return [
    { text: isZh ? "概览" : "Overview", link: `${base}/` },
    ...resourceItems(prefix, skill),
  ];
}

function buildSidebar(prefix: string): SidebarItem[] {
  const isZh = prefix.startsWith("/zh");
  return [
    {
      text: isZh ? "开始使用" : "Getting Started",
      items: [
        { text: isZh ? "介绍" : "Introduction", link: isZh ? "/zh/" : "/" },
        {
          text: isZh ? "安装" : "Installation",
          link: `${isZh ? "/zh" : ""}/installation`,
        },
        {
          text: isZh ? "快速开始" : "Quick Start",
          link: `${isZh ? "/zh" : ""}/quick-start`,
        },
        {
          text: isZh ? "使用指南" : "Usage",
          link: `${isZh ? "/zh" : ""}/usage`,
        },
      ],
    },
    {
      text: isZh ? "技能目录" : "Skill Index",
      items: [
        {
          text: isZh ? "全部技能" : "All Skills",
          link: `${isZh ? "/zh" : ""}/skills/`,
        },
      ],
    },
    {
      text: isZh
        ? "英文论文 (latex-paper-en)"
        : "English Papers (latex-paper-en)",
      collapsed: false,
      items: skillItems(prefix, "latex-paper-en"),
    },
    {
      text: isZh
        ? "中文学位论文 (latex-thesis-zh)"
        : "Chinese Thesis (latex-thesis-zh)",
      collapsed: false,
      items: skillItems(prefix, "latex-thesis-zh"),
    },
    {
      text: isZh ? "Typst 论文 (typst-paper)" : "Typst Papers (typst-paper)",
      collapsed: false,
      items: skillItems(prefix, "typst-paper"),
    },
    {
      text: isZh
        ? "Bib 文献检索 (bib-search-citation)"
        : "Bib Search (bib-search-citation)",
      collapsed: false,
      items: skillItems(prefix, "bib-search-citation"),
    },
    {
      text: isZh ? "投稿信 (cover-letter)" : "Cover Letters (cover-letter)",
      collapsed: false,
      items: skillItems(prefix, "cover-letter"),
    },
    {
      text: isZh ? "论文审查 (paper-audit)" : "Paper Audit (paper-audit)",
      collapsed: false,
      items: skillItems(prefix, "paper-audit"),
    },
  ];
}

// ---------------------------------------------------------------------------
// Main config
// ---------------------------------------------------------------------------

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Academic Writing Skills",
  description:
    "Skill-first documentation for LaTeX, Typst, bibliography search, paper audit, and academic cover-letter workflows",

  // Base URL for GitHub Pages
  base: "/academic-writing-skills/",

  // Check dead links natively
  ignoreDeadLinks: false,

  // Keep local search focused on task-facing docs. Large archived analyses and
  // long-form reference pages stay browsable, but they do not need to bloat
  // the generated search index chunks.
  transformPageData(pageData) {
    if (excludeFromLocalSearch(pageData.relativePath)) {
      pageData.frontmatter.search = false;
      return {
        frontmatter: {
          ...pageData.frontmatter,
          search: false,
        },
      };
    }
  },

  vite: {
    build: {
      // VitePress local search emits one prebuilt index chunk per locale.
      // In this bilingual docs site those chunks are content payloads, not
      // accidental vendor bloat, and they legitimately exceed Vite's default
      // 500 kB warning threshold.
      chunkSizeWarningLimit: 750,
    },
  },

  // Theme configuration
  themeConfig: {
    logo: "/logo.svg",
    siteTitle: "Academic Writing Skills",

    // Navigation
    nav: [
      { text: "Home", link: "/" },
      { text: "Installation", link: "/installation" },
      { text: "Skills", link: "/skills/" },
      { text: "Cover Letter", link: "/skills/cover-letter/" },
      { text: "Usage", link: "/usage" },
      {
        text: "GitHub",
        link: "https://github.com/bahayonghang/academic-writing-skills",
      },
    ],

    // Sidebar
    sidebar: buildSidebar(P),

    // Social links
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/bahayonghang/academic-writing-skills",
      },
    ],

    // Footer
    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © 2024-present Academic Writing Skills",
    },

    // Search
    search: {
      provider: "local",
      options: {
        // VitePress local search builds its index by rendering raw Markdown,
        // before transformPageData frontmatter mutations are visible. Filter
        // long reference/resource pages at render time so only task-facing
        // entry pages enter the local MiniSearch payload.
        _render(src, env, md) {
          if (excludeFromLocalSearch(env.relativePath)) {
            return "";
          }
          return md.render(src, env);
        },
      },
    },

    // Edit link
    editLink: {
      pattern:
        "https://github.com/bahayonghang/academic-writing-skills/edit/main/docs/:path",
      text: "Edit this page on GitHub",
    },
  },

  // Internationalization
  locales: {
    root: {
      label: "English",
      lang: "en",
    },
    zh: {
      label: "简体中文",
      lang: "zh-CN",
      link: "/zh/",
      themeConfig: {
        nav: [
          { text: "首页", link: "/zh/" },
          { text: "安装", link: "/zh/installation" },
          { text: "技能", link: "/zh/skills/" },
          { text: "投稿信", link: "/zh/skills/cover-letter/" },
          { text: "使用", link: "/zh/usage" },
          {
            text: "GitHub",
            link: "https://github.com/bahayonghang/academic-writing-skills",
          },
        ],
        sidebar: buildSidebar(PZH),
        editLink: {
          pattern:
            "https://github.com/bahayonghang/academic-writing-skills/edit/main/docs/:path",
          text: "在 GitHub 上编辑此页",
        },
        footer: {
          message: "基于 MIT 许可发布",
          copyright: "版权所有 © 2024-present Academic Writing Skills",
        },
        docFooter: {
          prev: "上一页",
          next: "下一页",
        },
        outline: {
          label: "页面导航",
        },
        lastUpdated: {
          text: "最后更新于",
          formatOptions: {
            dateStyle: "short",
            timeStyle: "medium",
          },
        },
        langMenuLabel: "多语言",
        returnToTopLabel: "回到顶部",
        sidebarMenuLabel: "菜单",
        darkModeSwitchLabel: "主题",
        lightModeSwitchTitle: "切换到浅色模式",
        darkModeSwitchTitle: "切换到深色模式",
      },
    },
  },

  // Markdown configuration
  markdown: {
    theme: {
      light: "github-light",
      dark: "github-dark",
    },
    lineNumbers: true,
  },

  // Head configuration
  head: [
    ["link", { rel: "icon", type: "image/svg+xml", href: "/logo.svg" }],
    ["meta", { name: "theme-color", content: "#0066cc" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:locale", content: "en" }],
    [
      "meta",
      {
        property: "og:title",
        content:
          "Academic Writing Skills | LaTeX, Typst, Paper Audit, Bibliography, and Cover Letter Workflows",
      },
    ],
    ["meta", { property: "og:site_name", content: "Academic Writing Skills" }],
    [
      "meta",
      {
        property: "og:url",
        content: "https://github.com/bahayonghang/academic-writing-skills",
      },
    ],
  ],
});
