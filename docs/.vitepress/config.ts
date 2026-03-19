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
    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Introduction', link: '/' },
          { text: 'Installation', link: '/installation' },
          { text: 'Quick Start', link: '/quick-start' }
        ]
      },
      {
        text: 'Skill Index',
        items: [
          { text: 'All Skills', link: '/skills/' }
        ]
      },
      {
        text: 'English Papers (latex-paper-en)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/latex-paper-en/' }
        ]
      },
      {
        text: 'Chinese Thesis (latex-thesis-zh)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/latex-thesis-zh/' }
        ]
      },
      {
        text: 'Typst Papers (typst-paper)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/typst-paper/' }
        ]
      },
      {
        text: 'Paper Audit (paper-audit)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/paper-audit/' },
          { text: 'Workflow', link: '/skills/paper-audit/resources/WORKFLOW' },
          { text: 'Modes', link: '/skills/paper-audit/resources/MODES' },
          { text: 'Outputs', link: '/skills/paper-audit/resources/OUTPUTS' },
          { text: 'CLI & Examples', link: '/skills/paper-audit/resources/CLI_AND_EXAMPLES' },
          { text: 'Troubleshooting', link: '/skills/paper-audit/resources/TROUBLESHOOTING' }
        ]
      },
      {
        text: 'Industrial AI Research',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/industrial-ai-research/' }
        ]
      }
    ],

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
        sidebar: [
          {
            text: '开始使用',
            items: [
              { text: '介绍', link: '/zh/' },
              { text: '安装', link: '/zh/installation' },
              { text: '快速开始', link: '/zh/quick-start' }
            ]
          },
          {
            text: '技能目录',
            items: [
              { text: '全部技能', link: '/zh/skills/' }
            ]
          },
          {
            text: '英文论文 (latex-paper-en)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/latex-paper-en/' }
            ]
          },
          {
            text: '中文论文 (latex-thesis-zh)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/latex-thesis-zh/' }
            ]
          },
          {
            text: 'Typst 论文 (typst-paper)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/typst-paper/' }
            ]
          },
          {
            text: '论文审查 (paper-audit)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/paper-audit/' },
              { text: '工作流', link: '/zh/skills/paper-audit/resources/WORKFLOW' },
              { text: '模式说明', link: '/zh/skills/paper-audit/resources/MODES' },
              { text: '输出产物', link: '/zh/skills/paper-audit/resources/OUTPUTS' },
              { text: '命令与示例', link: '/zh/skills/paper-audit/resources/CLI_AND_EXAMPLES' },
              { text: '常见问题', link: '/zh/skills/paper-audit/resources/TROUBLESHOOTING' }
            ]
          },
          {
            text: 'Industrial AI 调研',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/industrial-ai-research/' }
            ]
          }
        ],
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
