import { defineConfig } from 'vitepress'

function excludeFromLocalSearch(relativePath: string): boolean {
  const normalized = relativePath.replace(/\\/g, '/')

  return (
    normalized.startsWith('plans/') ||
    normalized.startsWith('report/') ||
    normalized.includes('/resources/references/') ||
    normalized.includes('resources/references/')
  )
}

// ---------------------------------------------------------------------------
// Sidebar helpers
// ---------------------------------------------------------------------------

const P = '/skills'
const PZH = '/zh/skills'

function latexPaperEnItems(prefix: string) {
  const base = `${prefix}/latex-paper-en`
  const m = `${base}/resources/modules`
  const r = `${base}/resources/references`
  return [
    { text: prefix.startsWith('/zh') ? '概览' : 'Overview', link: `${base}/` },
    {
      text: prefix.startsWith('/zh') ? '模块' : 'Modules',
      collapsed: true,
      items: [
        { text: 'Abstract', link: `${m}/ABSTRACT` },
        { text: 'Adapt', link: `${m}/ADAPT` },
        { text: 'Bibliography', link: `${m}/BIBLIOGRAPHY` },
        { text: 'Caption', link: `${m}/CAPTION` },
        { text: 'Compile', link: `${m}/COMPILE` },
        { text: 'DeAI', link: `${m}/DEAI` },
        { text: 'Experiment', link: `${m}/EXPERIMENT` },
        { text: 'Expression', link: `${m}/EXPRESSION` },
        { text: 'Format', link: `${m}/FORMAT` },
        { text: 'Grammar', link: `${m}/GRAMMAR` },
        { text: 'Logic', link: `${m}/LOGIC` },
        { text: 'Pseudocode', link: `${m}/PSEUDOCODE` },
        { text: 'Sentences', link: `${m}/SENTENCES` },
        { text: 'Tables', link: `${m}/TABLES` },
        { text: 'Title', link: `${m}/TITLE` },
        { text: 'Translation', link: `${m}/TRANSLATION` },
        { text: 'Workflow', link: `${m}/WORKFLOW` },
      ],
    },
    {
      text: prefix.startsWith('/zh') ? '参考资料' : 'References',
      collapsed: true,
      items: [
        { text: 'Abstract Structure', link: `${r}/ABSTRACT_STRUCTURE` },
        { text: 'Best Practices', link: `${r}/BEST_PRACTICES` },
        { text: 'Citation Styles', link: `${r}/CITATION_STYLES` },
        { text: 'Citation Verification', link: `${r}/CITATION_VERIFICATION` },
        { text: 'Common Errors', link: `${r}/COMMON_ERRORS` },
        { text: 'Compilation', link: `${r}/COMPILATION` },
        { text: 'DeAI Guide', link: `${r}/DEAI_GUIDE` },
        { text: 'Forbidden Terms', link: `${r}/FORBIDDEN_TERMS` },
        { text: 'Journal Abbreviations', link: `${r}/JOURNAL_ABBREVIATIONS` },
        { text: 'Journal Adaptation', link: `${r}/JOURNAL_ADAPTATION_WORKFLOW` },
        { text: 'Number & Unit Guide', link: `${r}/NUMBER_UNIT_GUIDE` },
        { text: 'Reviewer Perspective', link: `${r}/REVIEWER_PERSPECTIVE` },
        { text: 'Style Guide', link: `${r}/STYLE_GUIDE` },
        { text: 'Table Guide', link: `${r}/TABLE_GUIDE` },
        { text: 'Terminology', link: `${r}/TERMINOLOGY` },
        { text: 'Translation Guide', link: `${r}/TRANSLATION_GUIDE` },
        { text: 'Venues', link: `${r}/VENUES` },
        { text: 'Writing Philosophy', link: `${r}/WRITING_PHILOSOPHY` },
      ],
    },
  ]
}

function latexThesisZhItems(prefix: string) {
  const base = `${prefix}/latex-thesis-zh`
  const m = `${base}/resources/modules`
  const r = `${base}/resources`
  return [
    { text: prefix.startsWith('/zh') ? '概览' : 'Overview', link: `${base}/` },
    {
      text: prefix.startsWith('/zh') ? '模块' : 'Modules',
      collapsed: true,
      items: [
        { text: 'Abstract', link: `${m}/ABSTRACT` },
        { text: 'Bibliography', link: `${m}/BIBLIOGRAPHY` },
        { text: 'Compile', link: `${m}/COMPILE` },
        { text: 'Consistency', link: `${m}/CONSISTENCY` },
        { text: 'DeAI', link: `${m}/DEAI` },
        { text: 'Experiment', link: `${m}/EXPERIMENT` },
        { text: 'Format', link: `${m}/FORMAT` },
        { text: 'Logic', link: `${m}/LOGIC` },
        { text: 'Tables', link: `${m}/TABLES` },
        { text: 'Template', link: `${m}/TEMPLATE` },
        { text: 'Title', link: `${m}/TITLE` },
      ],
    },
    {
      text: prefix.startsWith('/zh') ? '参考资料' : 'References',
      collapsed: true,
      items: [
        { text: 'Abstract Structure', link: `${r}/ABSTRACT_STRUCTURE` },
        { text: 'Academic Style ZH', link: `${r}/ACADEMIC_STYLE_ZH` },
        { text: 'Caption Guide', link: `${r}/CAPTION_GUIDE` },
        { text: 'Compilation', link: `${r}/COMPILATION` },
        { text: 'DeAI Guide', link: `${r}/DEAI_GUIDE` },
        { text: 'Forbidden Terms', link: `${r}/FORBIDDEN_TERMS` },
        { text: 'GB Standard', link: `${r}/GB_STANDARD` },
        { text: 'Logic Coherence', link: `${r}/LOGIC_COHERENCE` },
        { text: 'Structure Guide', link: `${r}/STRUCTURE_GUIDE` },
        { text: 'Table Guide', link: `${r}/TABLE_GUIDE` },
        { text: 'Title Optimization', link: `${r}/TITLE_OPTIMIZATION` },
        { text: 'Writing Philosophy', link: `${r}/WRITING_PHILOSOPHY_ZH` },
      ],
    },
    {
      text: prefix.startsWith('/zh') ? '高校模板' : 'University Templates',
      collapsed: true,
      items: [
        { text: 'Generic', link: `${r}/UNIVERSITIES/generic` },
        { text: 'PKU', link: `${r}/UNIVERSITIES/pku` },
        { text: 'Tsinghua', link: `${r}/UNIVERSITIES/tsinghua` },
        { text: 'Yanshan', link: `${r}/UNIVERSITIES/yanshan` },
      ],
    },
  ]
}

function typstPaperItems(prefix: string) {
  const base = `${prefix}/typst-paper`
  const m = `${base}/resources/modules`
  const r = `${base}/resources/references`
  return [
    { text: prefix.startsWith('/zh') ? '概览' : 'Overview', link: `${base}/` },
    {
      text: prefix.startsWith('/zh') ? '模块' : 'Modules',
      collapsed: true,
      items: [
        { text: 'Abstract', link: `${m}/ABSTRACT` },
        { text: 'Adapt', link: `${m}/ADAPT` },
        { text: 'Bibliography', link: `${m}/BIBLIOGRAPHY` },
        { text: 'Caption', link: `${m}/CAPTION` },
        { text: 'Compile', link: `${m}/COMPILE` },
        { text: 'DeAI', link: `${m}/DEAI` },
        { text: 'Experiment', link: `${m}/EXPERIMENT` },
        { text: 'Expression', link: `${m}/EXPRESSION` },
        { text: 'Format', link: `${m}/FORMAT` },
        { text: 'Grammar', link: `${m}/GRAMMAR` },
        { text: 'Logic', link: `${m}/LOGIC` },
        { text: 'Pseudocode', link: `${m}/PSEUDOCODE` },
        { text: 'Sentences', link: `${m}/SENTENCES` },
        { text: 'Tables', link: `${m}/TABLES` },
        { text: 'Title', link: `${m}/TITLE` },
        { text: 'Translation', link: `${m}/TRANSLATION` },
        { text: 'Workflow', link: `${m}/WORKFLOW` },
      ],
    },
    {
      text: prefix.startsWith('/zh') ? '参考资料' : 'References',
      collapsed: true,
      items: [
        { text: 'Abstract Structure', link: `${r}/ABSTRACT_STRUCTURE` },
        { text: 'Best Practices', link: `${r}/BEST_PRACTICES` },
        { text: 'Citation Styles', link: `${r}/CITATION_STYLES` },
        { text: 'Citation Verification', link: `${r}/CITATION_VERIFICATION` },
        { text: 'Common Errors', link: `${r}/COMMON_ERRORS` },
        { text: 'DeAI Guide', link: `${r}/DEAI_GUIDE` },
        { text: 'Reviewer Perspective', link: `${r}/REVIEWER_PERSPECTIVE` },
        { text: 'Style Guide', link: `${r}/STYLE_GUIDE` },
        { text: 'Table Guide', link: `${r}/TABLE_GUIDE` },
        { text: 'Templates', link: `${r}/TEMPLATES` },
        { text: 'Terminology', link: `${r}/TERMINOLOGY` },
        { text: 'Translation Guide', link: `${r}/TRANSLATION_GUIDE` },
        { text: 'Typst Syntax', link: `${r}/TYPST_SYNTAX` },
        { text: 'Venues', link: `${r}/VENUES` },
        { text: 'Writing Philosophy', link: `${r}/WRITING_PHILOSOPHY` },
      ],
    },
  ]
}

function paperAuditItems(prefix: string) {
  const base = `${prefix}/paper-audit`
  const r = `${base}/resources`
  const isZh = prefix.startsWith('/zh')
  return [
    { text: isZh ? '概览' : 'Overview', link: `${base}/` },
    { text: isZh ? '工作流' : 'Workflow', link: `${r}/WORKFLOW` },
    { text: isZh ? '模式说明' : 'Modes', link: `${r}/MODES` },
    { text: isZh ? '输出产物' : 'Outputs', link: `${r}/OUTPUTS` },
    { text: isZh ? '命令与示例' : 'CLI & Examples', link: `${r}/CLI_AND_EXAMPLES` },
    { text: isZh ? '深度审查标准' : 'Deep Review Criteria', link: `${r}/DEEP_REVIEW_CRITERIA` },
    { text: isZh ? '审查清单' : 'Checklist', link: `${r}/CHECKLIST` },
    { text: isZh ? '定性研究标准' : 'Qualitative Standards', link: `${r}/QUALITATIVE_STANDARDS` },
    { text: isZh ? '主编智能体' : 'Editor-in-Chief Agent', link: `${r}/editor_in_chief_agent` },
    { text: isZh ? '常见问题' : 'Troubleshooting', link: `${r}/TROUBLESHOOTING` },
  ]
}

function industrialAiItems(prefix: string) {
  const base = `${prefix}/industrial-ai-research`
  return [
    { text: prefix.startsWith('/zh') ? '概览' : 'Overview', link: `${base}/` },
  ]
}

function buildSidebar(prefix: string) {
  const isZh = prefix.startsWith('/zh')
  return [
    {
      text: isZh ? '开始使用' : 'Getting Started',
      items: [
        { text: isZh ? '介绍' : 'Introduction', link: isZh ? '/zh/' : '/' },
        { text: isZh ? '安装' : 'Installation', link: `${isZh ? '/zh' : ''}/installation` },
        { text: isZh ? '快速开始' : 'Quick Start', link: `${isZh ? '/zh' : ''}/quick-start` },
      ],
    },
    {
      text: isZh ? '技能目录' : 'Skill Index',
      items: [
        { text: isZh ? '全部技能' : 'All Skills', link: `${isZh ? '/zh' : ''}/skills/` },
      ],
    },
    {
      text: isZh ? '英文论文 (latex-paper-en)' : 'English Papers (latex-paper-en)',
      collapsed: false,
      items: latexPaperEnItems(prefix),
    },
    {
      text: isZh ? '中文论文 (latex-thesis-zh)' : 'Chinese Thesis (latex-thesis-zh)',
      collapsed: false,
      items: latexThesisZhItems(prefix),
    },
    {
      text: isZh ? 'Typst 论文 (typst-paper)' : 'Typst Papers (typst-paper)',
      collapsed: false,
      items: typstPaperItems(prefix),
    },
    {
      text: isZh ? '论文审查 (paper-audit)' : 'Paper Audit (paper-audit)',
      collapsed: false,
      items: paperAuditItems(prefix),
    },
    {
      text: isZh ? 'Industrial AI 调研' : 'Industrial AI Research',
      collapsed: false,
      items: industrialAiItems(prefix),
    },
  ]
}

// ---------------------------------------------------------------------------
// Main config
// ---------------------------------------------------------------------------

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Academic Writing Skills",
  description: "Skill-first documentation for LaTeX, Typst, paper audit, and Industrial AI research workflows",

  // Base URL for GitHub Pages
  base: '/academic-writing-skills/',

  // Check dead links natively
  ignoreDeadLinks: false,

  // Keep local search focused on task-facing docs. Large archived analyses and
  // long-form reference pages stay browsable, but they do not need to bloat
  // the generated search index chunks.
  transformPageData(pageData) {
    if (excludeFromLocalSearch(pageData.relativePath)) {
      pageData.frontmatter.search = false
    }
  },

  vite: {
    build: {
      // VitePress local search emits one prebuilt index chunk per locale.
      // In this bilingual docs site those chunks are content payloads, not
      // accidental vendor bloat, and they legitimately exceed Vite's default
      // 500 kB warning threshold.
      chunkSizeWarningLimit: 750
    }
  },

  // Theme configuration
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Academic Writing Skills',

    // Navigation
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Installation', link: '/installation' },
      { text: 'Skills', link: '/skills/' },
      { text: 'Usage', link: '/usage' },
      { text: 'GitHub', link: 'https://github.com/bahayonghang/academic-writing-skills' }
    ],

    // Sidebar
    sidebar: buildSidebar(P),

    // Social links
    socialLinks: [
      { icon: 'github', link: 'https://github.com/bahayonghang/academic-writing-skills' }
    ],

    // Footer
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present Academic Writing Skills'
    },

    // Search
    search: {
      provider: 'local'
    },

    // Edit link
    editLink: {
      pattern: 'https://github.com/bahayonghang/academic-writing-skills/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    }
  },

  // Internationalization
  locales: {
    root: {
      label: 'English',
      lang: 'en'
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: [
          { text: '首页', link: '/zh/' },
          { text: '安装', link: '/zh/installation' },
          { text: '技能', link: '/zh/skills/' },
          { text: '使用', link: '/zh/usage' },
          { text: 'GitHub', link: 'https://github.com/bahayonghang/academic-writing-skills' }
        ],
        sidebar: buildSidebar(PZH),
        editLink: {
          pattern: 'https://github.com/bahayonghang/academic-writing-skills/edit/main/docs/:path',
          text: '在 GitHub 上编辑此页'
        },
        footer: {
          message: '基于 MIT 许可发布',
          copyright: '版权所有 © 2024-present Academic Writing Skills'
        },
        docFooter: {
          prev: '上一页',
          next: '下一页'
        },
        outline: {
          label: '页面导航'
        },
        lastUpdated: {
          text: '最后更新于',
          formatOptions: {
            dateStyle: 'short',
            timeStyle: 'medium'
          }
        },
        langMenuLabel: '多语言',
        returnToTopLabel: '回到顶部',
        sidebarMenuLabel: '菜单',
        darkModeSwitchLabel: '主题',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式'
      }
    }
  },

  // Markdown configuration
  markdown: {
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    },
    lineNumbers: true
  },

  // Head configuration
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' }],
    ['meta', { name: 'theme-color', content: '#0066cc' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:locale', content: 'en' }],
    ['meta', { property: 'og:title', content: 'Academic Writing Skills | Professional LaTeX Tools for Claude Code' }],
    ['meta', { property: 'og:site_name', content: 'Academic Writing Skills' }],
    ['meta', { property: 'og:url', content: 'https://github.com/bahayonghang/academic-writing-skills' }]
  ]
})
