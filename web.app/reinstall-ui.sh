#!/bin/bash

# 删除现有ui文件夹
rm -rf src/lib/components/ui

# 重新安装所有组件
pnpm dlx shadcn-svelte@next add alert avatar badge breadcrumb button card carousel collapsible dialog drawer dropdown-menu hover-card input label pagination popover range-calendar resizable scroll-area select separator sheet sidebar skeleton sonner switch tabs textarea tooltip