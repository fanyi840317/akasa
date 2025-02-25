<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
  import { Clock, MapPin, User, Shield, Eye, MessageSquare, Heart, UserPlus } from 'lucide-svelte';
  import { mockEvents } from '$lib/data/mock-events';
  import { mockUsers } from '$lib/data/mock-users';
  import Comments from '$lib/components/Comments.svelte';
  import EventTimeline from '$lib/components/EventTimeline.svelte';
  import JoinInvestigationForm from '$lib/components/JoinInvestigationForm.svelte';
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Tabs from "$lib/components/ui/tabs";
  
  // 从模拟数据中获取事件
  const event = mockEvents.find(e => e.id === $page.params.id);
  if (!event) throw new Error('Event not found');

  // 获取创建者信息
  const creator = mockUsers.find(u => u.id === event.createdBy);
  if (!creator) throw new Error('Creator not found');

  // 关注状态
  let isFollowing = false;
  let followersCount = creator.followers || 0;
  let isLiked = false;

  // 切换关注状态
  function toggleFollow() {
    isFollowing = !isFollowing;
    followersCount += isFollowing ? 1 : -1;
    // TODO: 实现实际的关注/取消关注逻辑
  }

  // 切换收藏状态
  function toggleLike() {
    isLiked = !isLiked;
    event.follows += isLiked ? 1 : -1;
    // TODO: 实现实际的收藏/取消收藏逻辑
  }

  // 滚动到评论区
  function scrollToComments() {
    const commentsSection = document.querySelector('#comments-section');
    if (commentsSection) {
      commentsSection.scrollIntoView({ behavior: 'smooth' });
    }
  }
  
// 申请表单状态
let showJoinForm = false;

// 处理申请提交
function handleJoinSubmit(data) {

  // console.log('提交申请:', { eventId: event.id, ...data });
  // TODO: 实现申请提交逻辑
  showJoinForm = false;
}
</script>

<!-- 封面区域 -->
<div class="relative w-full h-[60vh] mb-8">
  <div class="absolute inset-0">
    <img src={event.coverImage} alt={event.title} class="w-full h-full object-cover" />
    <div class="absolute inset-0 bg-background/60 backdrop-blur-sm"></div>
  </div>

  <!-- 核心信息区域 -->
  <div class="absolute inset-0 flex items-center justify-center">
    <div class="container max-w-4xl mx-auto px-4 space-y-8">
      <div class="space-y-6 text-center">
       

        <!-- 标签列表 -->
        <div class="flex flex-wrap justify-center gap-2">
          {#each event.tags as tag}
            <Badge variant="outline" class="bg-background/80 backdrop-blur-sm">{tag}</Badge>
          {/each}
        </div>
        
        <div>
          <h1 class="text-4xl font-bold mb-4">{event.title}</h1>
          <p class="text-xl text-muted-foreground">{event.description}</p>
        </div>

        <div class="flex justify-center gap-6 text-sm text-muted-foreground">
          <div class="flex items-center gap-2">
            <Clock class="w-5 h-5" />
            <span>{event.occurredAt.toLocaleString()}</span>
          </div>
          <div class="flex items-center gap-2">
            <MapPin class="w-5 h-5" />
            <span>{event.location.name}</span>
          </div>

        </div>

        <!-- 可信度指标 -->
        <div class="grid grid-cols-3 gap-4 mt-8">
          <div class="flex items-center gap-4 p-6 rounded-lg bg-background/80 backdrop-blur-md">
            <Shield class="w-8 h-8 text-primary" />
            <div>
              <div class="text-sm font-medium text-muted-foreground">{$_('events.credibility')}</div>
              <div class="text-3xl font-bold text-primary">{event.credibilityScore}%</div>
            </div>
          </div>
          
          <div class="flex items-center gap-4 p-6 rounded-lg bg-background/80 backdrop-blur-md">
            <div class="w-8 h-8 rounded-full flex items-center justify-center bg-accent/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 8v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <polyline points="9 11 12 14 15 11"/>
              </svg>
            </div>
            <div>
              <div class="text-sm font-medium text-muted-foreground">{$_('events.evidence_strength')}</div>
              <div class="text-2xl font-bold text-accent-foreground">{event.evidenceStrength}%</div>
            </div>
          </div>
          
          <div class="flex items-center gap-4 p-6 rounded-lg bg-background/80 backdrop-blur-md">
            <div class="w-8 h-8 rounded-full flex items-center justify-center bg-secondary/20">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div>
              <div class="text-sm font-medium text-muted-foreground">{$_('events.witness_credibility')}</div>
              <div class="text-2xl font-bold text-secondary-foreground">{event.witnessCredibility}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="container mx-auto flex gap-8">
  <div class="flex-1 space-y-6">

    <!-- 主要内容区域 -->
    <div class="space-y-8">
      <!-- 事件概述 -->
      <Card class="p-4">
        <div class="space-y-3">
           <!-- 创建者信息 -->
        <div class="flex items-center w-full justify-between">
          <div class="flex items-center gap-2">
            <Avatar class="w-10 h-10 ring-2 ring-primary/20">
              <AvatarImage src={creator.avatar} alt={creator.name} />
              <AvatarFallback>{creator.name.slice(0, 2)}</AvatarFallback>
            </Avatar>
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="font-medium hover:text-primary cursor-pointer transition-colors">{creator.name}</span>
                <Badge variant="outline" class="bg-primary/10">{creator.badges[0]}</Badge>
              </div>
              <div class="text-xs text-muted-foreground flex items-center gap-2">
                <span>调查等级 {creator.level}</span>
                <span>·</span>
                <span>{creator.investigations} 次调查</span>
                <span>·</span>
                <span>{followersCount} 位关注者</span>
              </div>
            </div>
          </div>
          <Button
            variant={isFollowing ? "secondary" : "default"}
            size="sm"
            class="gap-1"
            on:click={toggleFollow}
          >
            <UserPlus class="w-4 h-4" />
            {isFollowing ? '已关注' : '关注'}
          </Button>
        </div>
          <p class="text-muted-foreground leading-relaxed py-4">
            这是一起发生在{event.location.name}的{$_(`events.categories.${event.category}`)}事件。
            事件发生于{event.occurredAt.toLocaleString()}，持续时间约4分钟。
            在此期间，共有{event.witnesses.length}位目击者在春熙路商圈及周边区域观察到这一现象。
            目击者描述看到一个明亮的光球在夜空中移动，呈现出不寻常的运动轨迹和脉冲式闪烁特征。
            该事件目前的可信度评分为{event.credibilityScore}%，已收集到包括视频、照片和音频在内的多项证据。
          </p>
          <!-- 统计信息 -->
        <div class="flex items-center gap-6 text-sm text-muted-foreground">
          <div class="flex items-center gap-2">
            <Eye class="w-4 h-4" />
            <span>{event.views} 次浏览</span>
          </div>
          <button
            class="flex items-center gap-2 hover:text-primary transition-colors"
            class:text-primary={isLiked}
            on:click={toggleLike}
          >
            <Heart class="w-4 h-4" fill={isLiked ? "currentColor" : "none"} />
            <span>{event.follows} 次收藏</span>
          </button>
          <button
            class="flex items-center gap-2 hover:text-primary transition-colors"
            on:click={scrollToComments}
          >
            <MessageSquare class="w-4 h-4" />
            <span>{event.comments} 条评论</span>
          </button>
        </div>
        </div>
      </Card>

      <!-- 时间线和目击者标签页 -->
        <Tabs.Root value="timeline" class="w-full">
          <Tabs.List>
            <Tabs.Trigger value="timeline">时间线</Tabs.Trigger>
            <Tabs.Trigger value="witnesses">目击者</Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content value="timeline">
            
      <Card class="p-4">
            <EventTimeline {event} />
            </Card>
          </Tabs.Content>
          <Tabs.Content value="witnesses">
            
            
      <Card class="p-4">
            <div class="space-y-4 mt-4">
              {#each event.witnesses as witness}
                <div class="p-4 rounded-lg bg-secondary/10">
                  <div class="flex items-center gap-3 mb-2">
                    <Avatar class="w-10 h-10">
                      <AvatarFallback>{witness.anonymous ? '?' : witness.name[0]}</AvatarFallback>
                    </Avatar>
                    <div class="flex-1">
                      <div class="flex items-center gap-2">
                        <span class="font-medium">{witness.anonymous ? '匿名目击者' : witness.name}</span>
                        <Badge variant="outline" class="bg-primary/10">可信度 {witness.credibilityScore}%</Badge>
                      </div>
                    </div>
                  </div>
                  <p class="text-muted-foreground">{witness.testimony}</p>
                </div>
              {/each}
            </div>
      </Card>
          </Tabs.Content>
        </Tabs.Root>

      <!-- 统计信息和评论区域 -->
      <div class="space-y-6 py-4">
        

        <!-- 评论区域 -->
        <Comments
          comments={event.comments}
          onSubmit={(content) => {
            console.log('提交评论:', content);
            // TODO: 实现评论提交逻辑
          }}
        />
      </div>
    </div>
  </div>

  <!-- 右侧信息栏 -->
  <div class="w-80 space-y-6">
    <!-- 调查员列表 -->
    <Card class="p-4">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-semibold">{$_('events.investigators')}</h3>
        <Button variant="outline" size="sm" class="gap-1" on:click={() => showJoinForm = true}>
          <UserPlus class="w-4 h-4" />
          {$_('events.join_investigation')}
        </Button>
      </div>
      
      <div class="space-y-3">
        {#each event.investigators || [] as investigator}
          <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-accent/10">
            <Avatar class="w-8 h-8">
              <AvatarImage src={investigator.avatar} alt={investigator.name} />
              <AvatarFallback>{investigator.name.slice(0, 2)}</AvatarFallback>
            </Avatar>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-medium truncate">{investigator.name}</span>
                <Badge variant="outline" class="bg-primary/10">{investigator.role || '调查员'}</Badge>
              </div>
              <div class="text-xs text-muted-foreground">
                加入于 {new Date(investigator.joinedAt).toLocaleDateString()}
              </div>
            </div>
          </div>
        {/each}
      </div>
    </Card>

    <!-- 热门事件 -->
    <Card class="p-4">
      <h3 class="font-semibold mb-3">{$_('events.hot_events')}</h3>
      <div class="space-y-4">
        {#each mockEvents.slice(0, 5) as hotEvent}
          <a href="/events/{hotEvent.id}" class="block hover:bg-accent/10 rounded-lg p-2 transition-colors">
            <div class="flex gap-3">
              <div class="w-16 h-16 rounded-lg overflow-hidden bg-muted">
                <img src={hotEvent.image} alt={hotEvent.title} class="w-full h-full object-cover" />
              </div>
              <div class="flex-1">
                <div class="text-sm font-medium mb-1">{hotEvent.title}</div>
                <div class="text-xs text-muted-foreground line-clamp-2">{hotEvent.description}</div>
                <div class="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                  <div class="flex items-center gap-1">
                    <Eye class="w-3 h-3" />
                    <span>{hotEvent.views}</span>
                  </div>
                  <div class="flex items-center gap-1">
                    <MessageSquare class="w-3 h-3" />
                    <span>{hotEvent.comments}</span>
                  </div>
                </div>
              </div>
            </div>
          </a>
        {/each}
      </div>
    </Card>


  </div>
</div>

<!-- 申请表单弹窗 -->
<Dialog.Root bind:open={showJoinForm}>
  <Dialog.Content class="sm:max-w-[425px]">
    <Dialog.Header>
      <Dialog.Title>{$_('events.join_investigation')}</Dialog.Title>
      <Dialog.Description>
        {$_('events.join_investigation_description')}
      </Dialog.Description>
    </Dialog.Header>
    <JoinInvestigationForm
      eventId={event.id}
      onClose={() => showJoinForm = false}
      onSubmit={handleJoinSubmit}
    />
  </Dialog.Content>
</Dialog.Root>
