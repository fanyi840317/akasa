<script lang="ts">
    let {
        cancelText = "取消",
        confirmText = "保存",
        onCancel = () => {},
        onConfirm = () => {},
    } = $props<{
        cancelText?: string;
        confirmText?: string;
        onCancel?: () => void;
        onConfirm?: () => void;
    }>();

    function handleCancel() {
        onCancel();
    }

    function handleConfirm() {
        onConfirm();
    }
</script>

<div class="modal-action my-4 px-4">
    <button class="btn btn-sm btn-ghost" onclick={handleCancel}
        >{cancelText}</button
    >
    <button class="btn btn-sm btn-primary" onclick={handleConfirm}>
        {confirmText}
    </button>
</div>
