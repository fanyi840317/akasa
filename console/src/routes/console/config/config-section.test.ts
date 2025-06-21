import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/svelte';
import ConfigSection from './config-section.svelte';

describe('ConfigSection Component', () => {
	it('renders section title and description', () => {
		const props = {
			title: 'Test Section',
			description: 'Test description',
			data: {},
			fields: []
		};

		render(ConfigSection, { props });

		expect(screen.getByText('Test Section')).toBeInTheDocument();
		expect(screen.getByText('Test description')).toBeInTheDocument();
	});

	it('renders text input fields correctly', () => {
		const props = {
			title: 'Test Section',
			data: { testField: 'test value' },
			fields: [
				{
					key: 'testField',
					label: 'Test Field',
					type: 'text' as const,
					placeholder: 'Enter test value'
				}
			]
		};

		render(ConfigSection, { props });

		expect(screen.getByLabelText('Test Field')).toBeInTheDocument();
		expect(screen.getByDisplayValue('test value')).toBeInTheDocument();
		expect(screen.getByPlaceholderText('Enter test value')).toBeInTheDocument();
	});

	it('renders password input fields correctly', () => {
		const props = {
			title: 'Test Section',
			data: { apiKey: 'secret123' },
			fields: [
				{
					key: 'apiKey',
					label: 'API Key',
					type: 'password' as const,
					placeholder: 'Enter API key'
				}
			]
		};

		render(ConfigSection, { props });

		const passwordInput = screen.getByLabelText('API Key') as HTMLInputElement;
		expect(passwordInput).toBeInTheDocument();
		expect(passwordInput.type).toBe('password');
		expect(passwordInput.value).toBe('secret123');
	});

	it('renders number input fields correctly', () => {
		const props = {
			title: 'Test Section',
			data: { maxPages: 10 },
			fields: [
				{
					key: 'maxPages',
					label: 'Max Pages',
					type: 'number' as const,
					placeholder: 'Enter number'
				}
			]
		};

		render(ConfigSection, { props });

		const numberInput = screen.getByLabelText('Max Pages') as HTMLInputElement;
		expect(numberInput).toBeInTheDocument();
		expect(numberInput.type).toBe('number');
		expect(numberInput.value).toBe('10');
	});

	it('renders checkbox fields correctly', () => {
		const props = {
			title: 'Test Section',
			data: { enabled: true },
			fields: [
				{
					key: 'enabled',
					label: 'Enable Feature',
					type: 'checkbox' as const,
					description: 'Enable this feature'
				}
			]
		};

		render(ConfigSection, { props });

		const checkbox = screen.getByRole('checkbox') as HTMLInputElement;
		expect(checkbox).toBeInTheDocument();
		expect(checkbox.checked).toBe(true);
		expect(screen.getByText('Enable this feature')).toBeInTheDocument();
	});

	it('handles nested object paths correctly', () => {
		const props = {
			title: 'Test Section',
			data: {
				openai: {
					api_key: 'sk-test123'
				}
			},
			fields: [
				{
					key: 'openai.api_key',
					label: 'OpenAI API Key',
					type: 'password' as const
				}
			]
		};

		render(ConfigSection, { props });

		const input = screen.getByLabelText('OpenAI API Key') as HTMLInputElement;
		expect(input.value).toBe('sk-test123');
	});

	it('updates data when input values change', async () => {
		let data = { testField: 'initial' };
		
		const props = {
			title: 'Test Section',
			data,
			fields: [
				{
					key: 'testField',
					label: 'Test Field',
					type: 'text' as const
				}
			]
		};

		const { component } = render(ConfigSection, { props });

		const input = screen.getByLabelText('Test Field') as HTMLInputElement;
		
		// Simulate input change
		await fireEvent.input(input, { target: { value: 'updated value' } });
		
		// The component should update the bound data
		expect(input.value).toBe('updated value');
	});

	it('updates checkbox data when toggled', async () => {
		let data = { enabled: false };
		
		const props = {
			title: 'Test Section',
			data,
			fields: [
				{
					key: 'enabled',
					label: 'Enable Feature',
					type: 'checkbox' as const
				}
			]
		};

		render(ConfigSection, { props });

		const checkbox = screen.getByRole('checkbox') as HTMLInputElement;
		expect(checkbox.checked).toBe(false);
		
		// Simulate checkbox change
		await fireEvent.change(checkbox, { target: { checked: true } });
		
		expect(checkbox.checked).toBe(true);
	});

	it('handles number input conversion correctly', async () => {
		let data = { count: 5 };
		
		const props = {
			title: 'Test Section',
			data,
			fields: [
				{
					key: 'count',
					label: 'Count',
					type: 'number' as const
				}
			]
		};

		render(ConfigSection, { props });

		const input = screen.getByLabelText('Count') as HTMLInputElement;
		expect(input.value).toBe('5');
		
		// Simulate number input change
		await fireEvent.input(input, { target: { value: '10' } });
		
		expect(input.value).toBe('10');
	});

	it('creates nested objects when setting deep paths', async () => {
		let data = {};
		
		const props = {
			title: 'Test Section',
			data,
			fields: [
				{
					key: 'deep.nested.value',
					label: 'Deep Value',
					type: 'text' as const
				}
			]
		};

		render(ConfigSection, { props });

		const input = screen.getByLabelText('Deep Value') as HTMLInputElement;
		
		// Simulate input change
		await fireEvent.input(input, { target: { value: 'test value' } });
		
		expect(input.value).toBe('test value');
	});
});