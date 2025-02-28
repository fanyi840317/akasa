<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
  import { Card } from "$lib/components/ui/card";
  import { UserMinus } from "lucide-svelte";

  // 模拟关注列表数据
  let followingList = [
    {
      id: 1,
      name: '张三',
      avatar: null,
      bio: '热心市民',
      followedAt: new Date('2024-01-15')
    },
    {
      id: 2,
      name: '李四',
      avatar: null,
      bio: '正义使者',
      followedAt: new Date('2024-01-10')
    }
  ];

  function unfollowUser(userId: number) {
    // TODO: 实现取消关注逻辑
    console.log('取消关注用户:', userId);
    followingList = followingList.filter(user => user.id !== userId);
  }
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h3 class="text-lg font-medium">{$_('profile.following')}</h3>
      <p class="text-sm text-muted-foreground">{$_('profile.following_desc')}</p>
    </div>
  </div>

  <div class="grid gap-4">
    {#each followingList as user (user.id)}
      <Card class="p-4">
        <div class="flex items-start justify-between">
          <div class="flex items-start space-x-4">
            <Avatar class="h-12 w-12">
              {#if user.avatar}
                <AvatarImage src={user.avatar} alt={user.name} />
              {/if}
              <AvatarFallback>{user.name[0]}</AvatarFallback>
            </Avatar>
            <div class="space-y-1">
              <h4 class="text-sm font-semibold">{user.name}</h4>
              <p class="text-sm text-muted-foreground">{user.bio}</p>
              <p class="text-xs text-muted-foreground">
                {$_('profile.followed_at')} {user.followedAt.toLocaleDateString()}
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            class="text-muted-foreground hover:text-destructive"
            on:click={() => unfollowUser(user.id)}
          >
            <UserMinus class="h-4 w-4" />
          </Button>
        </div>
      </Card>
    {/each}

    {#if followingList.length === 0}
      <div class="text-center py-8 text-muted-foreground">
        {$_('profile.no_following')}
      </div>
    {/if}
  </div>
</div>