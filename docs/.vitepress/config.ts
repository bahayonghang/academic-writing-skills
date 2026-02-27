import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Academic Writing Skills",
  description: "Professional LaTeX and Typst academic writing skills for Claude Code",

  // Base URL for GitHub Pages
  base: '/academic-writing-skills/',

  // Check dead links natively
  ignoreDeadLinks: false,

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
        text: 'English Papers (latex-paper-en)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/latex-paper-en/' },
          {
            text: 'Modules', collapsed: true, items: [
              { text: 'Compile', link: '/skills/latex-paper-en/resources/modules/COMPILE' },
              { text: 'Format Check', link: '/skills/latex-paper-en/resources/modules/FORMAT' },
              { text: 'Grammar', link: '/skills/latex-paper-en/resources/modules/GRAMMAR' },
              { text: 'Long Sentences', link: '/skills/latex-paper-en/resources/modules/SENTENCES' },
              { text: 'Academic Expression', link: '/skills/latex-paper-en/resources/modules/EXPRESSION' },
              { text: 'Translation', link: '/skills/latex-paper-en/resources/modules/TRANSLATION' },
              { text: 'Bibliography', link: '/skills/latex-paper-en/resources/modules/BIBLIOGRAPHY' },
              { text: 'De-AI Polishing', link: '/skills/latex-paper-en/resources/modules/DEAI' },
              { text: 'Logic & Methodology', link: '/skills/latex-paper-en/resources/modules/LOGIC' },
              { text: 'Title Optimization', link: '/skills/latex-paper-en/resources/modules/TITLE' },
              { text: 'Workflow', link: '/skills/latex-paper-en/resources/modules/WORKFLOW' }
            ]
          },
          {
            text: 'References', collapsed: true, items: [
              { text: 'Style Guide', link: '/skills/latex-paper-en/resources/references/STYLE_GUIDE' },
              { text: 'Common Errors', link: '/skills/latex-paper-en/resources/references/COMMON_ERRORS' },
              { text: 'Venues', link: '/skills/latex-paper-en/resources/references/VENUES' },
              { text: 'Forbidden Terms', link: '/skills/latex-paper-en/resources/references/FORBIDDEN_TERMS' },
              { text: 'Terminology', link: '/skills/latex-paper-en/resources/references/TERMINOLOGY' },
              { text: 'Translation Guide', link: '/skills/latex-paper-en/resources/references/TRANSLATION_GUIDE' },
              { text: 'De-AI Guide', link: '/skills/latex-paper-en/resources/references/DEAI_GUIDE' },
              { text: 'Compilation', link: '/skills/latex-paper-en/resources/references/COMPILATION' },
              { text: 'Citation Verification', link: '/skills/latex-paper-en/resources/references/CITATION_VERIFICATION' },
              { text: 'Reviewer Perspective', link: '/skills/latex-paper-en/resources/references/REVIEWER_PERSPECTIVE' },
              { text: 'Writing Philosophy', link: '/skills/latex-paper-en/resources/references/WRITING_PHILOSOPHY' },
              { text: 'Best Practices', link: '/skills/latex-paper-en/resources/references/BEST_PRACTICES' }
            ]
          }
        ]
      },
      {
        text: 'Chinese Thesis (latex-thesis-zh)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/latex-thesis-zh/' },
          {
            text: 'Resources', collapsed: true, items: [
              { text: 'Academic Style (ZH)', link: '/skills/latex-thesis-zh/resources/ACADEMIC_STYLE_ZH' },
              { text: 'Compilation', link: '/skills/latex-thesis-zh/resources/COMPILATION' },
              { text: 'De-AI (ZH)', link: '/skills/latex-thesis-zh/resources/DEAI_GUIDE' },
              { text: 'Forbidden Terms', link: '/skills/latex-thesis-zh/resources/FORBIDDEN_TERMS' },
              { text: 'GB/T 7714 Format', link: '/skills/latex-thesis-zh/resources/GB_STANDARD' },
              { text: 'Logic & Coherence', link: '/skills/latex-thesis-zh/resources/LOGIC_COHERENCE' },
              { text: 'Structure Guide', link: '/skills/latex-thesis-zh/resources/STRUCTURE_GUIDE' },
              { text: 'Title Optimization', link: '/skills/latex-thesis-zh/resources/TITLE_OPTIMIZATION' },
              { text: 'Writing Philosophy (ZH)', link: '/skills/latex-thesis-zh/resources/WRITING_PHILOSOPHY_ZH' }
            ]
          }
        ]
      },
      {
        text: 'Paper Audit (paper-audit)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/paper-audit/' }
        ]
      },
      {
        text: 'Typst Papers (typst-paper)',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/skills/typst-paper/' },
          {
            text: 'Modules', collapsed: true, items: [
              { text: 'Compile', link: '/skills/typst-paper/resources/modules/COMPILE' },
              { text: 'Format Check', link: '/skills/typst-paper/resources/modules/FORMAT' },
              { text: 'Grammar', link: '/skills/typst-paper/resources/modules/GRAMMAR' },
              { text: 'Long Sentences', link: '/skills/typst-paper/resources/modules/SENTENCES' },
              { text: 'Academic Expression', link: '/skills/typst-paper/resources/modules/EXPRESSION' },
              { text: 'Translation', link: '/skills/typst-paper/resources/modules/TRANSLATION' },
              { text: 'Bibliography', link: '/skills/typst-paper/resources/modules/BIBLIOGRAPHY' },
              { text: 'De-AI Polishing', link: '/skills/typst-paper/resources/modules/DEAI' },
              { text: 'Logic & Methodology', link: '/skills/typst-paper/resources/modules/LOGIC' },
              { text: 'Title Optimization', link: '/skills/typst-paper/resources/modules/TITLE' },
              { text: 'Workflow', link: '/skills/typst-paper/resources/modules/WORKFLOW' }
            ]
          },
          {
            text: 'References', collapsed: true, items: [
              { text: 'Typst Syntax', link: '/skills/typst-paper/resources/references/TYPST_SYNTAX' },
              { text: 'Templates', link: '/skills/typst-paper/resources/references/TEMPLATES' },
              { text: 'Style Guide', link: '/skills/typst-paper/resources/references/STYLE_GUIDE' },
              { text: 'Common Errors', link: '/skills/typst-paper/resources/references/COMMON_ERRORS' },
              { text: 'Venues', link: '/skills/typst-paper/resources/references/VENUES' },
              { text: 'Terminology', link: '/skills/typst-paper/resources/references/TERMINOLOGY' },
              { text: 'Translation Guide', link: '/skills/typst-paper/resources/references/TRANSLATION_GUIDE' },
              { text: 'De-AI Guide', link: '/skills/typst-paper/resources/references/DEAI_GUIDE' },
              { text: 'Citation Verification', link: '/skills/typst-paper/resources/references/CITATION_VERIFICATION' },
              { text: 'Reviewer Perspective', link: '/skills/typst-paper/resources/references/REVIEWER_PERSPECTIVE' },
              { text: 'Writing Philosophy', link: '/skills/typst-paper/resources/references/WRITING_PHILOSOPHY' },
              { text: 'Best Practices', link: '/skills/typst-paper/resources/references/BEST_PRACTICES' }
            ]
          }
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
            text: '英文论文 (latex-paper-en)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/latex-paper-en/' },
              {
                text: '核心模块', collapsed: true, items: [
                  { text: '编译', link: '/zh/skills/latex-paper-en/resources/modules/COMPILE' },
                  { text: '格式检查', link: '/zh/skills/latex-paper-en/resources/modules/FORMAT' },
                  { text: '语法', link: '/zh/skills/latex-paper-en/resources/modules/GRAMMAR' },
                  { text: '长难句', link: '/zh/skills/latex-paper-en/resources/modules/SENTENCES' },
                  { text: '学术表达', link: '/zh/skills/latex-paper-en/resources/modules/EXPRESSION' },
                  { text: '学术翻译', link: '/zh/skills/latex-paper-en/resources/modules/TRANSLATION' },
                  { text: '参考文献', link: '/zh/skills/latex-paper-en/resources/modules/BIBLIOGRAPHY' },
                  { text: '去AI化', link: '/zh/skills/latex-paper-en/resources/modules/DEAI' },
                  { text: '逻辑与方法论', link: '/zh/skills/latex-paper-en/resources/modules/LOGIC' },
                  { text: '标题优化', link: '/zh/skills/latex-paper-en/resources/modules/TITLE' },
                  { text: '完整工作流', link: '/zh/skills/latex-paper-en/resources/modules/WORKFLOW' }
                ]
              },
              {
                text: '参考资料', collapsed: true, items: [
                  { text: '学术写作规范', link: '/zh/skills/latex-paper-en/resources/references/STYLE_GUIDE' },
                  { text: '常见中式英语', link: '/zh/skills/latex-paper-en/resources/references/COMMON_ERRORS' },
                  { text: '期刊与会议要求', link: '/zh/skills/latex-paper-en/resources/references/VENUES' },
                  { text: '禁用术语', link: '/zh/skills/latex-paper-en/resources/references/FORBIDDEN_TERMS' },
                  { text: '专业词汇表', link: '/zh/skills/latex-paper-en/resources/references/TERMINOLOGY' },
                  { text: '学术翻译指南', link: '/zh/skills/latex-paper-en/resources/references/TRANSLATION_GUIDE' },
                  { text: '去AI化指南', link: '/zh/skills/latex-paper-en/resources/references/DEAI_GUIDE' },
                  { text: '编译指南', link: '/zh/skills/latex-paper-en/resources/references/COMPILATION' },
                  { text: '引用核实验证', link: '/zh/skills/latex-paper-en/resources/references/CITATION_VERIFICATION' },
                  { text: '审稿人视角', link: '/zh/skills/latex-paper-en/resources/references/REVIEWER_PERSPECTIVE' },
                  { text: '写作哲学', link: '/zh/skills/latex-paper-en/resources/references/WRITING_PHILOSOPHY' },
                  { text: '最佳实践', link: '/zh/skills/latex-paper-en/resources/references/BEST_PRACTICES' }
                ]
              }
            ]
          },
          {
            text: '中文论文 (latex-thesis-zh)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/latex-thesis-zh/' },
              {
                text: '参考资料', collapsed: true, items: [
                  { text: '学术表达 (中文)', link: '/zh/skills/latex-thesis-zh/resources/ACADEMIC_STYLE_ZH' },
                  { text: '编译指南', link: '/zh/skills/latex-thesis-zh/resources/COMPILATION' },
                  { text: '去AI化指南', link: '/zh/skills/latex-thesis-zh/resources/DEAI_GUIDE' },
                  { text: '受保护术语', link: '/zh/skills/latex-thesis-zh/resources/FORBIDDEN_TERMS' },
                  { text: 'GB/T 国标规范', link: '/zh/skills/latex-thesis-zh/resources/GB_STANDARD' },
                  { text: '逻辑与方法论', link: '/zh/skills/latex-thesis-zh/resources/LOGIC_COHERENCE' },
                  { text: '结构规范', link: '/zh/skills/latex-thesis-zh/resources/STRUCTURE_GUIDE' },
                  { text: '标题优化指南', link: '/zh/skills/latex-thesis-zh/resources/TITLE_OPTIMIZATION' },
                  { text: '写作哲学 (中文)', link: '/zh/skills/latex-thesis-zh/resources/WRITING_PHILOSOPHY_ZH' }
                ]
              }
            ]
          },
          {
            text: 'Typst 论文 (typst-paper)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/typst-paper/' },
              {
                text: '核心模块', collapsed: true, items: [
                  { text: '编译', link: '/zh/skills/typst-paper/resources/modules/COMPILE' },
                  { text: '格式检查', link: '/zh/skills/typst-paper/resources/modules/FORMAT' },
                  { text: '语法', link: '/zh/skills/typst-paper/resources/modules/GRAMMAR' },
                  { text: '长难句', link: '/zh/skills/typst-paper/resources/modules/SENTENCES' },
                  { text: '学术表达', link: '/zh/skills/typst-paper/resources/modules/EXPRESSION' },
                  { text: '学术翻译', link: '/zh/skills/typst-paper/resources/modules/TRANSLATION' },
                  { text: '参考文献', link: '/zh/skills/typst-paper/resources/modules/BIBLIOGRAPHY' },
                  { text: '去AI化', link: '/zh/skills/typst-paper/resources/modules/DEAI' },
                  { text: '逻辑与方法论', link: '/zh/skills/typst-paper/resources/modules/LOGIC' },
                  { text: '标题优化', link: '/zh/skills/typst-paper/resources/modules/TITLE' },
                  { text: '完整工作流', link: '/zh/skills/typst-paper/resources/modules/WORKFLOW' }
                ]
              },
              {
                text: '参考资料', collapsed: true, items: [
                  { text: 'Typst 语法指南', link: '/zh/skills/typst-paper/resources/references/TYPST_SYNTAX' },
                  { text: '会议/期刊模板', link: '/zh/skills/typst-paper/resources/references/TEMPLATES' },
                  { text: '学术写作规范', link: '/zh/skills/typst-paper/resources/references/STYLE_GUIDE' },
                  { text: '常见错误', link: '/zh/skills/typst-paper/resources/references/COMMON_ERRORS' },
                  { text: '期刊与会议要求', link: '/zh/skills/typst-paper/resources/references/VENUES' },
                  { text: '专业词汇表', link: '/zh/skills/typst-paper/resources/references/TERMINOLOGY' },
                  { text: '学术翻译指南', link: '/zh/skills/typst-paper/resources/references/TRANSLATION_GUIDE' },
                  { text: '去AI化指南', link: '/zh/skills/typst-paper/resources/references/DEAI_GUIDE' },
                  { text: '引用核实验证', link: '/zh/skills/typst-paper/resources/references/CITATION_VERIFICATION' },
                  { text: '审稿人视角', link: '/zh/skills/typst-paper/resources/references/REVIEWER_PERSPECTIVE' },
                  { text: '写作哲学', link: '/zh/skills/typst-paper/resources/references/WRITING_PHILOSOPHY' },
                  { text: '最佳实践', link: '/zh/skills/typst-paper/resources/references/BEST_PRACTICES' }
                ]
              }
            ]
          },
          {
            text: '论文审查 (paper-audit)',
            collapsed: false,
            items: [
              { text: '概览', link: '/zh/skills/paper-audit/' }
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
