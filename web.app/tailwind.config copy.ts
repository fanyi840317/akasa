@tailwind base;
@tailwind components;
@tailwind utilities;

/* Geist Font Definition (保留) */
@font-face {
  font-family: 'Geist';
  src: url('/fonts/Geist/geist.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

/* 您可能需要添加其他字体的 @font-face (如果本地托管) */
/* @font-face { ... inter ... } */
/* @font-face { ... suisse ... } */
/* @font-face { ... fira-mono ... } */


@layer base {
  :root {
    /* --- Light Theme (使用 lb-marketing light 的值) --- */
    /* 从 lb-* CSS 的 [data-theme=light] 或默认 :root 中提取 */
    --background: 0 0% 100%;    /* --lb-marketing-color-background-surface-base-inverse (因为 light mode 下 marketing 的 base 是 #000) */
    --foreground: 0 0% 0%;      /* --lb-marketing-color-text-inverse */
    --card: 0 0% 100%;          /* --lb-marketing-color-background-surface-base-inverse */
    --card-foreground: 0 0% 0%; /* --lb-marketing-color-text-inverse */
    --popover: 0 0% 100%;       /* --lb-marketing-color-background-surface-base-inverse */
    --popover-foreground: 0 0% 0%; /* --lb-marketing-color-text-inverse */
    --primary: 251 79% 71%;     /* --lb-marketing-color-text-brand: #8f6cef */
    --primary-foreground: 0 0% 100%; /* --lb-marketing-color-fill: #fff */
    --secondary: 256 2% 99% / 0.08; /* --lb-marketing-color-background-surface-faded-subtle: hsla(256,2%,99%,.08) - marketing light 没有直接的 secondary，用 faded 替代 */
    --secondary-foreground: 256 1% 41%; /* --lb-marketing-color-text-subtle: #68676b */
    --muted: 256 2% 99% / 0.05; /* --lb-marketing-color-background-surface-divider-subtlest: hsla(256,2%,99%,.05) */
    --muted-foreground: 257 1% 58%; /* --lb-marketing-color-text-subtler: #949296 */
    --accent: 251 79% 71% / 0.15; /* --lb-marketing-color-background-surface-brand-subtle: rgba(122,81,236,.15) */
    --accent-foreground: 251 79% 71%; /* --lb-marketing-color-text-brand: #8f6cef */
    --destructive: 358 91% 64%;  /* --lb-marketing-color-text-danger: #f54545 */
    --destructive-foreground: 0 0% 100%; /* --lb-marketing-color-fill: #fff */
    --border: 256 2% 99% / 0.11; /* --lb-marketing-color-border-divider: hsla(256,2%,99%,.11) */
    --input: 256 2% 99% / 0.11;  /* 同 border */
    --ring: 251 79% 71%;      /* --lb-marketing-color-border-divider-brand: #8f6cef */
    --radius: 0.5rem; /* 假设 marketing 使用 0.5rem */

    /* Sidebar (需要根据实际设计映射，这里是基于 marketing 的推测) */
    --sidebar-background: 0 0% 98%; /* 浅灰色背景 */
    --sidebar-foreground: 256 1% 41%; /* --lb-marketing-color-text-subtle */
    --sidebar-primary: 251 79% 71%; /* --lb-marketing-color-text-brand */
    --sidebar-primary-foreground: 0 0% 100%; /* white */
    --sidebar-accent: 256 2% 99% / 0.08; /* --lb-marketing-color-background-surface-faded-subtle */
    --sidebar-accent-foreground: 251 79% 71%; /* --lb-marketing-color-text-brand */
    --sidebar-border: 256 2% 99% / 0.13; /* --lb-marketing-color-border-divider-bold */
    --sidebar-ring: 251 79% 71%;      /* --lb-marketing-color-border-divider-brand */

    /* Font Variables */
    --font-sans: 'Geist', -apple-system, 'PingFang SC', 'Microsoft YaHei', 'Source Han Sans SC', sans-serif;
    --font-inter: '__inter_...'; /* 替换 */
    --font-suisse: '__suisse_...'; /* 替换 */
    --font-fira-mono: '__Fira_Mono_...'; /* 替换 */

    /* (可选) 保留原始 lb-* 变量 */
    /* ... */
  }

  .dark {
    /* --- Dark Theme (使用 lb-marketing dark 的值) --- */
    /* 从 lb-* CSS 的 [data-theme=dark] 或 prefers-color-scheme: dark 中提取 */
    --background: 0 0% 0%;       /* --lb-marketing-color-background-surface-base: #000 */
    --foreground: 0 0% 100%;     /* --lb-marketing-color-text: #fff */
    --card: 270 3% 7%;       /* --lb-marketing-color-background-surface-raised: #0f0f10 */
    --card-foreground: 0 0% 100%;  /* --lb-marketing-color-text: #fff */
    --popover: 270 3% 7%;      /* --lb-marketing-color-background-surface-raised: #0f0f10 */
    --popover-foreground: 0 0% 100%; /* --lb-marketing-color-text: #fff */
    --primary: 251 79% 71%;     /* --lb-marketing-color-text-brand: #8f6cef */
    --primary-foreground: 0 0% 100%; /* --lb-marketing-color-fill: #fff */
    --secondary: 256 2% 99% / 0.11; /* --lb-marketing-color-background-surface-faded: hsla(256,2%,99%,.11) */
    --secondary-foreground: 256 2% 71%; /* --lb-marketing-color-text-subtle: #b4b4b7 */
    --muted: 256 2% 99% / 0.08; /* --lb-marketing-color-background-surface-faded-subtle: hsla(256,2%,99%,.08) */
    --muted-foreground: 257 1% 56%; /* --lb-marketing-color-text-subtler: #8e8d91 */
    --accent: 251 79% 71% / 0.15; /* --lb-marketing-color-background-surface-brand-subtle: rgba(122,81,236,.15) */
    --accent-foreground: 251 79% 71%; /* --lb-marketing-color-text-brand: #8f6cef */
    --destructive: 0 84% 70%;   /* --lb-marketing-color-text-danger: #ef6c6c */
    --destructive-foreground: 0 0% 100%; /* --lb-marketing-color-fill: #fff */
    --border: 256 2% 99% / 0.11; /* --lb-marketing-color-border-divider: hsla(256,2%,99%,.11) */
    --input: 256 2% 99% / 0.11;  /* 同 border */
    --ring: 251 79% 71%;      /* --lb-marketing-color-border-divider-brand: #8f6cef */
    /* --radius 保持一致 */

    /* Sidebar (需要根据实际设计映射，这里是基于 marketing dark 的推测) */
    --sidebar-background: 270 3% 7%;       /* --lb-marketing-color-background-surface-raised */
    --sidebar-foreground: 256 2% 71%; /* --lb-marketing-color-text-subtle */
    --sidebar-primary: 251 79% 71%;     /* --lb-marketing-color-text-brand */
    --sidebar-primary-foreground: 0 0% 100%; /* white */
    --sidebar-accent: 256 2% 99% / 0.13; /* --lb-marketing-color-background-surface-faded-bold */
    --sidebar-accent-foreground: 251 79% 71%; /* --lb-marketing-color-text-brand */
    --sidebar-border: 256 2% 99% / 0.13; /* --lb-marketing-color-border-divider-bold */
    --sidebar-ring: 251 79% 71%;      /* --lb-marketing-color-border-divider-brand */

    /* (可选) 保留原始 lb-* 变量 */
    /* ... */
  }
}

/* 基础样式应用 (移除全局边框) */
@layer base {
  /*  * { @apply border-border; }  <-- 已移除 */

  body {
    @apply bg-background text-foreground;
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  /* 可以从 lb-* CSS 文件中复制一些您需要的其他基础重置样式 */
  /* 例如:
  h1,h2,h3,h4,h5,h6{
    font-size:inherit;
    font-weight:inherit
  }
  a{
    color:inherit;
    text-decoration:inherit
  }
  */
}

/* 其他样式 (动画等) */
/* @keyframes Spinner_spin__CmdAF{...} */
/* .Spinner_bar__30T0c{...} */