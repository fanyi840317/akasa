const sdk = require('node-appwrite');

const client = new sdk.Client();
const databases = new sdk.Databases(client);

client
    .setEndpoint('https://cloud.appwrite.io/v1')
    .setProject('67ac15990027bfb157f9')
    .setKey("standard_122aa6dfe96e880578a6b9857e10dabcddca60f320f38cecd393fdaaedc080f2639432ddab4dcd652c21da0d4b75168f531ab0949a530594d07679df049127ea91f2f22251cd8ca2155aa2847d2c626de7ffbc42f9b0a9b640b534f3daee6eb1f9c3fb46fdb2d84dec6aea8476ef6709b5548e36be9a68ac4f2290925997f96c")

const DATABASE_ID = '67d3a4480018e2e09b68';
const COLLECTION_ID = 'cases';

const mysteryEvents = [
    {
        title: "深夜的地铁幽灵",
        cover: "https://images.unsplash.com/photo-1555661530-68c8e98db4e6",
        descrp: "多位乘客报告在午夜时分的地铁末班车上遇到一位穿着白色连衣裙的女性，但监控录像中却完全没有这个人的身影。",
        content: "2023年10月以来，在城市地铁3号线的末班车上，陆续有乘客报告遇到一位穿着白色连衣裙的神秘女性。据描述，这位女性总是独自站在车厢角落，面容模糊，且从不与人交谈。最令人不安的是，当调取地铁监控录像时，画面中完全没有这位女性的身影。\n\n目击者描述：\n- 张先生（10月15日）：'她就站在那里，我很确定看到了她，但当我想靠近时，她就消失了。'\n- 李女士（10月28日）：'那天车厢里只有我和她，我能感觉到异常的寒意。'\n- 王先生（11月3日）：'我用手机想拍下她，但照片里什么都没有。'\n\n地铁公司的回应是设备运行正常，未发现任何异常。但为了安全起见，已经加派了夜间安保人员。这个案件目前仍在调查中。",
        user_id: "system",
        happend_time: "2023-10-15 23:45:00",
        status: "investigating",
        priority: "high",
        category: "apparition",
        tags: "地铁,幽灵,都市传说"
    },
    {
        title: "消失的古董钟表",
        cover: "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5",
        descrp: "一座百年老宅中的古董座钟每到午夜都会准时报时，但实际检查时发现钟表的内部机芯早已损坏。",
        content: "在城市老城区的一座具有百年历史的宅院中，存在着一个令人费解的现象。一座维多利亚时期的古董座钟，尽管机芯已经完全锈蚀损坏，却仍然会在每天午夜准时发出12声报时声。\n\n这座宅院目前由陈家三代人居住。据陈家老人回忆，这座钟表是他祖父从英国带回来的，已有超过80年的历史。然而在2020年的一次例行保养中，钟表匠惊讶地发现，这座钟表的内部机芯已经完全损坏，按理说不可能发出任何声音。\n\n更为神秘的是，多位专业人士在午夜前后对钟表进行了详细检查和录音，却始终无法解释声音的来源。声音分析显示，报时声的音色和频率与正常的机械钟表完全一致。\n\n目前已知情况：\n1. 机芯确实已经损坏，无法运转\n2. 声音分析显示是真实的机械钟表声\n3. 现象仅在午夜出现\n4. 多个专业仪器都无法检测到声波的具体来源\n\n当地民俗专家认为这可能与宅院的历史有关，但具体原因仍在调查中。",
        user_id: "system",
        happend_time: "2020-12-01 00:00:00",
        status: "investigating",
        priority: "medium",
        category: "paranormal",
        tags: "古董,钟表,声音异常"
    },
    {
        title: "镜中世界的来信",
        cover: "https://images.unsplash.com/photo-1550537687-c91072c4792d",
        descrp: "一面普通的浴室镜子开始在表面显示神秘文字，内容似乎来自平行世界。",
        content: "2024年1月初，市区一个普通住宅小区的居民王女士报告了一个离奇的现象。她家浴室的镜子在每天早晨都会出现一些奇怪的文字，这些文字看起来像是某种信息。\n\n现象描述：\n- 文字总是在清晨5:30左右出现\n- 内容似乎是在描述另一个相似但又不同的世界\n- 文字会在阳光照射后逐渐消失\n- 用相机无法拍摄这些文字\n\n部分文字内容记录：\n'在这里，天空是绿色的，人们在空中行走。我们的世界与你们相似，却又如此不同。时间正在重叠，我们需要帮助...'\n\n专家检测结果：\n1. 镜子材质为普通玻璃，无特殊涂层\n2. 未检测到任何化学反应\n3. 房间温湿度正常\n4. 未发现任何投影设备\n\n目前已经有多位证人确认看到过这些文字，但科学仪器始终无法捕捉到它们的存在。这个案例引发了对平行宇宙理论的讨论。",
        user_id: "system",
        happend_time: "2024-01-05 05:30:00",
        status: "active",
        priority: "high",
        category: "dimensional",
        tags: "镜子,平行世界,神秘文字"
    },
    {
        title: "会预言的流浪猫",
        cover: "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba",
        descrp: "一只黑白相间的流浪猫通过特定行为准确预测了多次重大事件。",
        content: "从2023年下半年开始，城市中心公园附近出现了一只特殊的流浪猫。这只黑白相间的猫咪展现出了不同寻常的能力，似乎能够预知即将发生的重大事件。\n\n记录的预言事件：\n1. 9月15日：通过在特定建筑前持续徘徊，预警了一次可能的建筑安全隐患，工程检查后确实发现了严重的结构问题\n2. 10月23日：在地震发生前24小时，反常地带领其他流浪猫离开了某片区域，该区域后来成为地震重灾区\n3. 12月8日：通过特殊的叫声和行为模式，提前预示了一场重大交通事故的发生地点\n\n这只猫的特征：\n- 黑白相间的毛色\n- 左眼蓝色，右眼金色\n- 性格独立，很少与人亲近\n- 只在重大事件前出现\n\n目前多个研究机构正在尝试捕捉和研究这只猫，但它总是能够神秘地消失。当地居民已经开始将它视为城市的守护者。\n\n专家推测这可能与动物的特殊感知能力有关，但无法解释为什么只有这一只猫表现出如此准确的预知能力。",
        user_id: "system",
        happend_time: "2023-09-15 00:00:00",
        status: "monitoring",
        priority: "medium",
        category: "precognition",
        tags: "动物,预言,灵异"
    },
    {
        title: "记忆交换实验",
        cover: "https://images.unsplash.com/photo-1559757175-0eb30cd8c063",
        descrp: "两名毫无关联的陌生人声称在同一天早上醒来后拥有了对方的记忆。",
        content: "2024年2月1日，两名居住在城市不同区域的陌生人同时向警方报案，称他们可能发生了某种记忆交换现象。这两人分别是35岁的软件工程师张明和42岁的高中教师李芳。\n\n事件经过：\n- 两人都在1月31日晚正常入睡\n- 2月1日早晨醒来后，发现自己拥有了对方的记忆\n- 双方都能准确描述对方的生活细节、家庭情况和工作内容\n- 两人之前从未见过面，居住地相距超过20公里\n\n记忆交换的具体表现：\n1. 张明能够详细讲解李芳的课程内容和学生情况\n2. 李芳掌握了张明正在开发的项目细节和代码结构\n3. 双方都保留了自己的原有记忆，同时获得了对方的记忆\n\n专家调查发现：\n- 两人的脑电波出现某种程度的同步现象\n- 核磁共振显示大脑活动模式有异常\n- 双方都能通过测试证明自己掌握了对方的专业知识\n\n目前科学界无法解释这种现象。有人推测可能与量子纠缠或意识传输有关，但缺乏确切证据。两人目前在接受持续观察和研究。",
        user_id: "system",
        happend_time: "2024-02-01 06:00:00",
        status: "investigating",
        priority: "high",
        category: "consciousness",
        tags: "记忆,意识,超自然"
    }
];

async function initializeCases() {
    try {
        console.log("🚀 开始初始化神秘事件数据...");
        
        for (const event of mysteryEvents) {
            try {
                await databases.createDocument(
                    DATABASE_ID,
                    COLLECTION_ID,
                    sdk.ID.unique(),
                    event
                );
                console.log(`✅ 成功添加事件: ${event.title}`);
            } catch (error) {
                console.error(`❌ 添加事件 ${event.title} 失败:`, error.message || error);
            }
        }

        console.log("🎉 神秘事件数据初始化完成！");
    } catch (error) {
        console.error("❌ 初始化过程中发生错误:", error.message || error);
    }
}

// 运行初始化
initializeCases();