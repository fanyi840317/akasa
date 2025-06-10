import prettier from 'eslint-config-prettier';
import js from '@eslint/js';
import { includeIgnoreFile } from '@eslint/compat';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import { fileURLToPath } from 'node:url';
import ts from 'typescript-eslint';
import svelteConfig from './svelte.config.js';

const gitignorePath = fileURLToPath(new URL('./.gitignore', import.meta.url));

export default ts.config(
	includeIgnoreFile(gitignorePath),
	js.configs.recommended,
	...ts.configs.recommended,
	...svelte.configs.recommended,
	prettier,
	...svelte.configs.prettier,
	{
		languageOptions: {
			globals: { ...globals.browser, ...globals.node }
		},
		rules: {
			'no-undef': 'off',
			// 命名规则
			'@typescript-eslint/naming-convention': [
				'error',
				// 变量使用 camelCase
				{
					selector: 'variable',
					format: ['camelCase', 'PascalCase', 'UPPER_CASE']
				},
				// 函数使用 camelCase
				{
					selector: 'function',
					format: ['camelCase']
				},
				// 类使用 PascalCase
				{
					selector: 'class',
					format: ['PascalCase']
				},
				// 接口使用 PascalCase
				{
					selector: 'interface',
					format: ['PascalCase']
				},
				// 类型别名使用 PascalCase
				{
					selector: 'typeAlias',
					format: ['PascalCase']
				},
				// 枚举使用 PascalCase
				{
					selector: 'enum',
					format: ['PascalCase']
				},
				// 枚举成员使用 UPPER_CASE
				{
					selector: 'enumMember',
					format: ['UPPER_CASE']
				},
				// 方法使用 camelCase
				{
					selector: 'method',
					format: ['camelCase']
				},
				// 属性使用 camelCase，但允许对象字面量属性使用 kebab-case（用于 ESLint 规则名）
			{
				selector: 'property',
				format: ['camelCase', 'PascalCase', 'UPPER_CASE', 'kebab-case'],
				filter: {
					regex: '^[a-z]+(-[a-z]+)*$',
					match: false
				}
			},
			// 对象字面量属性允许 kebab-case（ESLint 规则名）
			{
				selector: 'objectLiteralProperty',
				format: ['camelCase', 'PascalCase', 'UPPER_CASE', 'kebab-case']
			},
				// 参数使用 camelCase
				{
					selector: 'parameter',
					format: ['camelCase']
				}
			]
		}
	},
	{
		files: ['**/*.svelte', '**/*.svelte.ts', '**/*.svelte.js'],
		languageOptions: {
			parserOptions: {
				projectService: true,
				extraFileExtensions: ['.svelte'],
				parser: ts.parser,
				svelteConfig
			}
		}
	}
);
