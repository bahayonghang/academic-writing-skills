import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Academic Writing Skills",
  description: "Professional LaTeX academic writing skills for Claude Code",

  // Base URL for GitHub Pages
  base: '/academic-writing-skills/',

  // Ignore dead links for now (guides pages not yet created)
  ignoreDeadLinks: true,

  // Theme configuration
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Academic Writing Skills',

    // Navigation
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Installation', link: '/installation' },
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
        text: 'Skills',
        items: [
          { text: 'English Papers (latex-paper-en)', link: '/skills/latex-paper-en' },
          { text: 'Chinese Thesis (latex-thesis-zh)', link: '/skills/latex-thesis-zh' }
        ]
      },
      {
        text: 'Guides',
        items: [
          { text: 'Compilation Recipes', link: '/guides/compilation' },
          { text: 'Format Checking', link: '/guides/format-checking' },
          { text: 'Bibliography Management', link: '/guides/bibliography' }
        ]
      },
      {
        text: 'References',
        items: [
          { text: 'Common Errors', link: '/references/common-errors' },
          { text: 'Style Guide', link: '/references/style-guide' },
          { text: 'Venues', link: '/references/venues' }
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
      lang: 'en',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/' },
          { text: 'Installation', link: '/installation' },
          { text: 'Usage', link: '/usage' },
          { text: 'GitHub', link: 'https://github.com/bahayonghang/academic-writing-skills' }
        ],
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
            text: 'Skills',
            items: [
              { text: 'English Papers (latex-paper-en)', link: '/skills/latex-paper-en' },
              { text: 'Chinese Thesis (latex-thesis-zh)', link: '/skills/latex-thesis-zh' }
            ]
          },
          {
            text: 'Guides',
            items: [
              { text: 'Compilation Recipes', link: '/guides/compilation' },
              { text: 'Format Checking', link: '/guides/format-checking' },
              { text: 'Bibliography Management', link: '/guides/bibliography' }
            ]
          },
          {
            text: 'References',
            items: [
              { text: 'Common Errors', link: '/references/common-errors' },
              { text: 'Style Guide', link: '/references/style-guide' },
              { text: 'Venues', link: '/references/venues' }
            ]
          }
        ]
      }
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: [
          { text: '首页', link: '/zh/' },
          { text: '安装', link: '/zh/installation' },
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
            text: '技能',
            items: [
              { text: '英文论文 (latex-paper-en)', link: '/zh/skills/latex-paper-en' },
              { text: '中文论文 (latex-thesis-zh)', link: '/zh/skills/latex-thesis-zh' }
            ]
          },
          {
            text: '指南',
            items: [
              { text: '编译配方', link: '/zh/guides/compilation' },
              { text: '格式检查', link: '/zh/guides/format-checking' },
              { text: '参考文献管理', link: '/zh/guides/bibliography' }
            ]
          },
          {
            text: '参考',
            items: [
              { text: '常见错误', link: '/zh/references/common-errors' },
              { text: '写作规范', link: '/zh/references/style-guide' },
              { text: '期刊会议', link: '/zh/references/venues' }
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
