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

function latexPaperEnItems(prefix: string) {
  const base = `${prefix}/latex-paper-en`;
  const m = `${base}/resources/modules`;
  const r = `${base}/resources/references`;
  return [
    { text: prefix.startsWith("/zh") ? "概览" : "Overview", link: `${base}/` },
    {
      text: prefix.startsWith("/zh") ? "模块" : "Modules",
      collapsed: true,
      items: [
        { text: "Abstract", link: `${m}/abstract` },
        { text: "Adapt", link: `${m}/adapt` },
        { text: "Bibliography", link: `${m}/bibliography` },
        { text: "Caption", link: `${m}/caption` },
        { text: "Figures", link: `${m}/figures` },
        { text: "Compile", link: `${m}/compile` },
        { text: "DeAI", link: `${m}/deai` },
        { text: "Experiment", link: `${m}/experiment` },
        { text: "Expression", link: `${m}/expression` },
        { text: "Format", link: `${m}/format` },
        { text: "Grammar", link: `${m}/grammar` },
        { text: "Logic", link: `${m}/logic` },
        { text: "Pseudocode", link: `${m}/pseudocode` },
        { text: "Section Writing", link: `${m}/section-writing` },
        { text: "Sentences", link: `${m}/sentences` },
        { text: "Tables", link: `${m}/tables` },
        { text: "Title", link: `${m}/title` },
        { text: "Translation", link: `${m}/translation` },
      ],
    },
    {
      text: prefix.startsWith("/zh") ? "参考资料" : "References",
      collapsed: true,
      items: [
        { text: "Abstract Structure", link: `${r}/writing/abstract-structure` },
        { text: "Best Practices", link: `${r}/writing/best-practices` },
        { text: "Citation Styles", link: `${r}/citations/styles` },
        { text: "Citation Verification", link: `${r}/citations/verification` },
        { text: "Common Errors", link: `${r}/writing/common-errors` },
        { text: "Compilation", link: `${r}/latex/compilation` },
        { text: "DeAI Guide", link: `${r}/deai/guide` },
        { text: "Forbidden Terms", link: `${r}/deai/forbidden-terms` },
        {
          text: "Journal Abbreviations",
          link: `${r}/citations/journal-abbreviations`,
        },
        {
          text: "Journal Adaptation",
          link: `${r}/venues/journal-adaptation-workflow`,
        },
        {
          text: "Number & Unit Guide",
          link: `${r}/formatting/number-unit-guide`,
        },
        {
          text: "Reviewer Perspective",
          link: `${r}/review/reviewer-perspective`,
        },
        { text: "Style Guide", link: `${r}/writing/style-guide` },
        { text: "Table Guide", link: `${r}/formatting/table-guide` },
        { text: "Terminology", link: `${r}/writing/terminology` },
        { text: "Translation Guide", link: `${r}/writing/translation-guide` },
        { text: "Venues", link: `${r}/venues/catalog` },
        { text: "Writing Philosophy", link: `${r}/writing/writing-philosophy` },
      ],
    },
    {
      text: prefix.startsWith("/zh") ? "分节写作" : "Section Writing",
      collapsed: true,
      items: [
        { text: "Index", link: `${r}/writing/section-writing/index` },
        { text: "Abstract", link: `${r}/writing/section-writing/abstract` },
        {
          text: "Introduction",
          link: `${r}/writing/section-writing/introduction`,
        },
        {
          text: "Related Work",
          link: `${r}/writing/section-writing/related-work`,
        },
        { text: "Method", link: `${r}/writing/section-writing/method` },
        {
          text: "Experiments",
          link: `${r}/writing/section-writing/experiments`,
        },
        { text: "Conclusion", link: `${r}/writing/section-writing/conclusion` },
        { text: "Flow", link: `${r}/writing/section-writing/flow` },
        {
          text: "Self Review",
          link: `${r}/writing/section-writing/self-review`,
        },
      ],
    },
  ];
}

function latexThesisZhItems(prefix: string) {
  const base = `${prefix}/latex-thesis-zh`;
  const m = `${base}/resources/modules`;
  const r = `${base}/resources`;
  return [
    { text: prefix.startsWith("/zh") ? "概览" : "Overview", link: `${base}/` },
    {
      text: prefix.startsWith("/zh") ? "模块" : "Modules",
      collapsed: true,
      items: [
        { text: "Structure", link: `${m}/structure` },
        { text: "Abstract", link: `${m}/abstract` },
        { text: "Bibliography", link: `${m}/bibliography` },
        { text: "Compile", link: `${m}/compile` },
        { text: "Consistency", link: `${m}/consistency` },
        { text: "DeAI", link: `${m}/deai` },
        { text: "Experiment", link: `${m}/experiment` },
        { text: "Format", link: `${m}/format` },
        { text: "Logic", link: `${m}/logic` },
        { text: "Literature", link: `${m}/literature` },
        { text: "References Check", link: `${m}/references` },
        { text: "Tables", link: `${m}/tables` },
        { text: "Template", link: `${m}/template` },
        { text: "Title", link: `${m}/title` },
      ],
    },
    {
      text: prefix.startsWith("/zh") ? "参考资料" : "References",
      collapsed: true,
      items: [
        { text: "Abstract Structure", link: `${r}/writing/abstract-structure` },
        { text: "Academic Style ZH", link: `${r}/writing/academic-style-zh` },
        { text: "Caption Guide", link: `${r}/formatting/caption-guide` },
        { text: "Compilation", link: `${r}/latex/compilation` },
        { text: "DeAI Guide", link: `${r}/deai/guide` },
        { text: "Forbidden Terms", link: `${r}/deai/forbidden-terms` },
        { text: "GB Standard", link: `${r}/citations/gb-standard` },
        { text: "Logic Coherence", link: `${r}/writing/logic-coherence` },
        { text: "Structure Guide", link: `${r}/writing/structure-guide` },
        { text: "Table Guide", link: `${r}/formatting/table-guide` },
        {
          text: "Thesis Writing Guide",
          link: `${r}/writing/thesis-writing-guide`,
        },
        { text: "Title Optimization", link: `${r}/writing/title-optimization` },
        {
          text: "Writing Philosophy",
          link: `${r}/writing/writing-philosophy-zh`,
        },
      ],
    },
    {
      text: prefix.startsWith("/zh") ? "高校模板" : "University Templates",
      collapsed: true,
      items: [
        { text: "Generic", link: `${r}/university-templates/generic` },
        { text: "PKU", link: `${r}/university-templates/pku` },
        { text: "Tsinghua", link: `${r}/university-templates/tsinghua` },
        { text: "Yanshan", link: `${r}/university-templates/yanshan` },
      ],
    },
  ];
}

function typstPaperItems(prefix: string) {
  const base = `${prefix}/typst-paper`;
  const m = `${base}/resources/modules`;
  const r = `${base}/resources/references`;
  return [
    { text: prefix.startsWith("/zh") ? "概览" : "Overview", link: `${base}/` },
    {
      text: prefix.startsWith("/zh") ? "模块" : "Modules",
      collapsed: true,
      items: [
        { text: "Abstract", link: `${m}/ABSTRACT` },
        { text: "Adapt", link: `${m}/ADAPT` },
        { text: "Bibliography", link: `${m}/BIBLIOGRAPHY` },
        { text: "Caption", link: `${m}/CAPTION` },
        { text: "Compile", link: `${m}/COMPILE` },
        { text: "DeAI", link: `${m}/DEAI` },
        { text: "Experiment", link: `${m}/EXPERIMENT` },
        { text: "Expression", link: `${m}/EXPRESSION` },
        { text: "Format", link: `${m}/FORMAT` },
        { text: "Grammar", link: `${m}/GRAMMAR` },
        { text: "Logic", link: `${m}/LOGIC` },
        { text: "Pseudocode", link: `${m}/PSEUDOCODE` },
        { text: "Sentences", link: `${m}/SENTENCES` },
        { text: "Tables", link: `${m}/TABLES` },
        { text: "Title", link: `${m}/TITLE` },
        { text: "Translation", link: `${m}/TRANSLATION` },
      ],
    },
    {
      text: prefix.startsWith("/zh") ? "参考资料" : "References",
      collapsed: true,
      items: [
        { text: "Abstract Structure", link: `${r}/ABSTRACT_STRUCTURE` },
        { text: "Best Practices", link: `${r}/BEST_PRACTICES` },
        { text: "Citation Styles", link: `${r}/CITATION_STYLES` },
        { text: "Citation Verification", link: `${r}/CITATION_VERIFICATION` },
        { text: "Common Errors", link: `${r}/COMMON_ERRORS` },
        { text: "DeAI Guide", link: `${r}/DEAI_GUIDE` },
        { text: "Reviewer Perspective", link: `${r}/REVIEWER_PERSPECTIVE` },
        { text: "Style Guide", link: `${r}/STYLE_GUIDE` },
        { text: "Table Guide", link: `${r}/TABLE_GUIDE` },
        { text: "Templates", link: `${r}/TEMPLATES` },
        { text: "Terminology", link: `${r}/TERMINOLOGY` },
        { text: "Translation Guide", link: `${r}/TRANSLATION_GUIDE` },
        { text: "Typst Syntax", link: `${r}/TYPST_SYNTAX` },
        { text: "Venues", link: `${r}/VENUES` },
        { text: "Writing Philosophy", link: `${r}/WRITING_PHILOSOPHY` },
      ],
    },
  ];
}

function bibSearchCitationItems(prefix: string) {
  const base = `${prefix}/bib-search-citation`;
  const r = `${base}/resources`;
  const isZh = prefix.startsWith("/zh");
  return [
    { text: isZh ? "概览" : "Overview", link: `${base}/` },
    { text: isZh ? "查询语法" : "Query Syntax", link: `${r}/query-syntax` },
  ];
}

function paperAuditItems(prefix: string) {
  const base = `${prefix}/paper-audit`;
  const r = `${base}/resources`;
  const isZh = prefix.startsWith("/zh");
  return [
    { text: isZh ? "概览" : "Overview", link: `${base}/` },
    { text: isZh ? "工作流" : "Workflow", link: `${r}/WORKFLOW` },
    { text: isZh ? "模式说明" : "Modes", link: `${r}/MODES` },
    { text: isZh ? "输出产物" : "Outputs", link: `${r}/OUTPUTS` },
    {
      text: isZh ? "命令与示例" : "CLI & Examples",
      link: `${r}/CLI_AND_EXAMPLES`,
    },
    {
      text: isZh ? "深度审查标准" : "Deep Review Criteria",
      link: `${r}/DEEP_REVIEW_CRITERIA`,
    },
    {
      text: isZh ? "投稿前机械规则" : "Pre-Submission Rules",
      link: `${r}/PRE_SUBMISSION_RULES`,
    },
    { text: isZh ? "审查清单" : "Checklist", link: `${r}/CHECKLIST` },
    {
      text: isZh ? "定性研究标准" : "Qualitative Standards",
      link: `${r}/QUALITATIVE_STANDARDS`,
    },
    {
      text: isZh ? "主编智能体" : "Editor-in-Chief Agent",
      link: `${r}/editor_in_chief_agent`,
    },
    {
      text: isZh ? "常见问题" : "Troubleshooting",
      link: `${r}/TROUBLESHOOTING`,
    },
  ];
}

function coverLetterItems(prefix: string) {
  const base = `${prefix}/cover-letter`;
  const isZh = prefix.startsWith("/zh");
  return [{ text: isZh ? "概览" : "Overview", link: `${base}/` }];
}

function buildSidebar(prefix: string) {
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
      items: latexPaperEnItems(prefix),
    },
    {
      text: isZh
        ? "中文论文 (latex-thesis-zh)"
        : "Chinese Thesis (latex-thesis-zh)",
      collapsed: false,
      items: latexThesisZhItems(prefix),
    },
    {
      text: isZh ? "Typst 论文 (typst-paper)" : "Typst Papers (typst-paper)",
      collapsed: false,
      items: typstPaperItems(prefix),
    },
    {
      text: isZh
        ? "Bib 文献检索 (bib-search-citation)"
        : "Bib Search (bib-search-citation)",
      collapsed: false,
      items: bibSearchCitationItems(prefix),
    },
    {
      text: isZh ? "投稿信 (cover-letter)" : "Cover Letters (cover-letter)",
      collapsed: false,
      items: coverLetterItems(prefix),
    },
    {
      text: isZh ? "论文审查 (paper-audit)" : "Paper Audit (paper-audit)",
      collapsed: false,
      items: paperAuditItems(prefix),
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
