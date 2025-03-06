<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import { Textarea } from "$lib/components/ui/textarea";
  import * as Dialog from "$lib/components/ui/dialog";

  export let eventId: string;
  export let onClose: () => void;
  export let onSubmit: (data: any) => void;

  let formData = {
    reason: '',
    experience: '',
    expertise: '',
    availability: ''
  };

  let errors = {
    reason: '',
    experience: '',
    expertise: '',
    availability: ''
  };

  function validateForm() {
    let isValid = true;
    errors = {
      reason: '',
      experience: '',
      expertise: '',
      availability: ''
    };

    if (!formData.reason.trim()) {
      errors.reason = '请填写申请理由';
      isValid = false;
    }

    if (!formData.experience.trim()) {
      errors.experience = '请填写相关经验';
      isValid = false;
    }

    if (!formData.expertise.trim()) {
      errors.expertise = '请填写个人专长';
      isValid = false;
    }

    if (!formData.availability.trim()) {
      errors.availability = '请填写时间投入';
      isValid = false;
    }

    return isValid;
  }

  function handleSubmit() {
    if (validateForm()) {
      onSubmit({ eventId, ...formData });
    }
  }
</script>

<form class="space-y-6" on:submit|preventDefault={handleSubmit}>
  <div class="space-y-4">
    <div class="space-y-2">
      <Label for="reason">申请理由</Label>
      <Textarea
        id="reason"
        bind:value={formData.reason}
        placeholder="请详细说明您为什么想要加入这项调查"
      />
      {#if errors.reason}
        <p class="text-sm text-destructive">{errors.reason}</p>
      {/if}
    </div>

    <div class="space-y-2">
      <Label for="experience">相关经验</Label>
      <Textarea
        id="experience"
        bind:value={formData.experience}
        placeholder="请描述您在类似调查中的经验"
      />
      {#if errors.experience}
        <p class="text-sm text-destructive">{errors.experience}</p>
      {/if}
    </div>

    <div class="space-y-2">
      <Label for="expertise">个人专长</Label>
      <Input
        id="expertise"
        bind:value={formData.expertise}
        placeholder="例如：数据分析、实地调查、摄影记录等"
      />
      {#if errors.expertise}
        <p class="text-sm text-destructive">{errors.expertise}</p>
      {/if}
    </div>

    <div class="space-y-2">
      <Label for="availability">时间投入</Label>
      <Input
        id="availability"
        bind:value={formData.availability}
        placeholder="您计划每周投入多少时间参与调查"
      />
      {#if errors.availability}
        <p class="text-sm text-destructive">{errors.availability}</p>
      {/if}
    </div>
  </div>

  <Dialog.Footer>
    <Button type="button" variant="outline" on:click={onClose}>取消</Button>
    <Button type="submit">提交申请</Button>
  </Dialog.Footer>
</form>