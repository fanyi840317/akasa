import { writable } from 'svelte/store';

type AlertType = 'confirm' | 'message';

interface AlertDialogOptions {
  type?: AlertType;
  title?: string;
  message?: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
}

interface AlertDialogState extends AlertDialogOptions {
  isOpen: boolean;
}

const initialState: AlertDialogState = {
  isOpen: false,
  type: 'confirm',
  title: '提示',
  message: '',
  confirmText: '确定',
  cancelText: '取消',
  onConfirm: () => {},
  onCancel: () => {}
};

const { subscribe, set, update } = writable<AlertDialogState>(initialState);

export const alertDialog = {
  subscribe,
  confirm: (options: Omit<AlertDialogOptions, 'type'> = {}) => {
    set({
      ...initialState,
      type: 'confirm',
      ...options,
      isOpen: true
    });
  },
  message: (options: Omit<AlertDialogOptions, 'type' | 'onCancel'> = {}) => {
    set({
      ...initialState,
      type: 'message',
      ...options,
      isOpen: true
    });
  },
  close: () => {
    update(state => ({
      ...state,
      isOpen: false
    }));
  }
}; 