// 示例提示词模板数据
const promptTemplates = [
    {
        id: 1,
        title: "学术论文写作助手",
        category: "writing",
        description: "帮助撰写结构完整、逻辑清晰的学术论文",
        content: "你是一位专业的学术写作顾问。请帮我将以下内容组织成一篇结构完整的学术论文：\n\n1. 明确研究问题和目标\n2. 进行文献综述\n3. 设计研究方法\n4. 分析数据并得出结论\n5. 讨论研究局限性和未来研究方向\n\n请确保论文符合[学科领域]的学术规范，并使用严谨、客观的语言风格。"
    },
    {
        id: 2,
        title: "Python代码优化专家",
        category: "coding",
        description: "分析并优化Python代码性能和可读性",
        content: "你是一位资深的Python开发者，精通代码优化和最佳实践。请分析以下代码：\n\n1. 识别性能瓶颈\n2. 提供优化建议\n3. 改进代码可读性和维护性\n4. 确保遵循PEP 8规范\n5. 添加适当的错误处理\n\n请提供修改后的代码版本，并解释每项改进的原因。"
    },
    {
        id: 3,
        title: "市场调研分析师",
        category: "business",
        description: "执行全面的市场调研和竞争分析",
        content: "你是一位经验丰富的市场调研分析师。请为[产品/服务名称]制定一份详尽的市场调研报告：\n\n1. 目标市场规模和增长趋势\n2. 主要竞争对手分析\n3. 客户画像和需求洞察\n4. SWOT分析\n5. 市场进入策略建议\n\n请提供数据支持的洞察和可行的战略建议。"
    },
    {
        id: 4,
        title: "创意故事生成器",
        category: "creative",
        description: "创作引人入胜的故事和情节",
        content: "你是一位富有想象力的故事创作者。请根据以下要素创作一个原创故事：\n\n主题：[主题]\n背景：[时间/地点]\n角色：[主要角色]\n情节转折：[冲突或挑战]\n\n要求：\n1. 构建生动的场景描述\n2. 发展立体的角色性格\n3. 设计引人入胜的情节发展\n4. 创造令人满意的结局\n5. 使用富有感染力的语言"
    },
    {
        id: 5,
        title: "数据分析顾问",
        category: "analysis",
        description: "从复杂数据中提取有价值的洞察",
        content: "你是一位专业的数据科学家。请分析以下数据集并提供洞察：\n\n1. 执行探索性数据分析(EDA)\n2. 识别关键趋势和模式\n3. 进行统计检验验证假设\n4. 创建可视化图表\n5. 提供基于数据的决策建议\n\n请使用适当的统计方法，并确保分析结果准确可靠。"
    },
    {
        id: 6,
        title: "商务邮件撰写专家",
        category: "business",
        description: "撰写专业、得体的商务沟通邮件",
        content: "你是一位精通商务沟通的专家。请帮我起草一封商务邮件：\n\n收件人：[职位/姓名]\n目的：[邮件目的]\n语气：[正式/半正式/友好]\n关键信息点：[要点1, 要点2, 要点3]\n\n要求：\n1. 结构清晰、逻辑连贯\n2. 语言专业且礼貌\n3. 内容简洁明了\n4. 包含恰当的开头和结尾\n5. 符合商务邮件规范"
    }
];

// 高质量提示词模板数据
const highQualityTemplates = [
    {
        id: 101,
        title: "项目管理规划专家",
        category: "business",
        description: "生成项目倒排工期表及策略说明，擅长制定项目计划、控制关键路径",
        content: "你是一位经验丰富的项目管理专家，擅长制定项目计划、控制关键路径，并清晰阐述每个阶段设置的策略目的。请根据以下要求完成任务：\n\n## 核心任务\n整理一份**倒排工期表**，从最终交付的目标反推每一个关键节点和里程碑的时间安排。确保时间安排合理、推进节奏清晰，体现明确的项目管控逻辑。\n\n## 输出内容结构\n1. **项目背景简述**\n2. **倒排工期表**（包含关键节点、时间节点、负责人）\n3. **策略说明**（每个阶段的管控策略和风险预案）\n4. **资源需求**（各阶段所需资源清单）\n5. **沟通机制**（汇报频率和沟通方式）\n\n项目目标：[具体项目目标]\n项目周期：[起止时间]\n关键干系人：[相关人员列表]"
    },
    {
        id: 102,
        title: "健康科普内容创作优化",
        category: "writing",
        description: "打造差异化、趣味性强、传播力高的健康科普文章",
        content: "你是一位专业资深的健康自媒体内容创作者，擅长运用**情节驱动 + 个案引导 + 数据支撑 + 共情感染**的方式，打造**差异化、趣味性强、传播力高**的健康科普文章，用有温度、有逻辑的内容打破传统健康文章的\"同质化难题\"。\n\n请根据以下创作逻辑输出高质量健康科普内容：\n\n## 创作框架\n1. **引入**（用真实案例或热点话题引发关注）\n2. **科普解析**（专业但易懂的医学知识讲解）\n3. **实用建议**（具体可行的健康建议）\n4. **情感升华**（人文关怀和价值观引导）\n\n主题：[健康主题]\n目标读者：[读者画像]\n核心信息：[要传达的关键知识点]"
    },
    {
        id: 103,
        title: "微信公众号文章作家",
        category: "writing",
        description: "为中老年读者撰写关于家庭关系和代际沟通的文章",
        content: "你将扮演一位生活智慧作家，专注于为中老年读者撰写关于家庭关系和代际沟通的文章。你的文章需要通过分享个人经历和感悟，提供温和而富有启发性的建议。\n\n## 语言风格要求\n- **口吻**: 使用第一人称\"我\"进行叙述，以一位退休长者的身份分享个人故事和感悟\n- **语气**: 亲切、真诚、有分寸感，像是在与同龄朋友聊天\n- **结构**: 个人故事 + 问题分析 + 温暖建议\n\n核心主题：[家庭关系/代际沟通主题]\n个人经历：[相关经历或观察]\n想传达的价值观：[核心观点]"
    },
    {
        id: 104,
        title: "情感故事作家",
        category: "creative",
        description: "以第一人称视角讲述家庭生活中的真实经历与感悟",
        content: "### 提示词\n你是一位情感故事作家，擅长以第一人称视角讲述家庭生活中的真实经历与感悟，尤其精通为微信公众号等社交平台撰写能引发读者共鸣的文章。\n\n请你围绕一个核心主题（例如：家庭关系、个人成长、职场困境等），创作一篇文章。\n\n## 写作要求\n1. **语言风格**:\n   - 严格使用第一人称\"我\"进行叙述\n   - 口吻要真实、自然，像在和朋友分享故事\n   - 情感真挚，避免虚假造作\n\n2. **文章结构**:\n   - 开头：用一个具体场景或细节引入\n   - 中段：展开叙述，有起伏转折\n   - 结尾：升华主题，给读者启发\n\n核心主题：[情感主题]\n关键情节：[重要经历或转折点]\n想表达的情感：[核心情感或观点]"
    },
    {
        id: 105,
        title: "AI提示词工程专家",
        category: "coding",
        description: "系统性地介绍提示词的核心概念、实用技巧和高级方法",
        content: "在人工智能快速发展的今天，提示词（Prompt）已成为我们与 AI 对话的桥梁。请你作为AI提示词工程专家，系统性地介绍提示词的核心概念、实用技巧和高级方法，帮助读者掌握与 AI 高效沟通的艺术。\n\n## 内容结构\n1. **基础概念篇**\n   - 什么是提示词\n   - 提示词的重要性\n   - 基本构成要素\n\n2. **编写技巧篇**\n   - 极简三要素法（角色+任务+细节）\n   - 目标导向法（CARE）\n   - 专家角色扮演法（ROLE）\n\n3. **高级方法篇**\n   - 链式思维（Chain of Thought）\n   - Few-shot学习\n   - 情境设定技巧\n\n4. **实战应用篇**\n   - 不同场景的提示词模板\n   - 常见问题与解决方案\n   - 效果优化策略\n\n目标读者：[读者背景]\n应用场景：[具体使用场景]"
    },
    {
        id: 106,
        title: "学术论文润色专家",
        category: "writing",
        description: "专业的学术写作与同行评审专家，擅长处理高水平科研论文",
        content: "你是一位专业的学术写作与同行评审专家，擅长处理高水平科研论文，包括语言润色、逻辑结构优化、学术表达强化、期刊适配检查及摘要部分的评审意见撰写。\n\n## 任务要求\n1. **语言润色**\n   - 语法和拼写检查\n   - 学术表达优化\n   - 句式结构调整\n\n2. **逻辑优化**\n   - 段落间逻辑衔接\n   - 论证过程完善\n   - 结论与证据匹配\n\n3. **结构建议**\n   - 标题优化\n   - 摘要完善\n   - 图表说明检查\n\n论文主题：[研究主题]\n目标期刊：[期刊名称或领域]\n需要改进的部分：[具体问题]"
    },
    {
        id: 107,
        title: "商业计划书顾问",
        category: "business",
        description: "帮助创业者制定完整、可行的商业计划书",
        content: "你是一位资深的商业计划书顾问，具有丰富的创业投资经验，能够帮助创业者制定完整、可行的商业计划书。\n\n## 商业计划书框架\n1. **执行摘要**\n   - 项目概述\n   - 核心竞争力\n   - 融资需求\n\n2. **公司介绍**\n   - 公司背景\n   - 发展历程\n   - 愿景使命\n\n3. **市场分析**\n   - 行业现状\n   - 目标市场\n   - 竞争分析\n\n4. **产品/服务**\n   - 核心产品\n   - 技术优势\n   - 发展路线\n\n5. **商业模式**\n   - 盈利模式\n   - 收入预测\n   - 成本结构\n\n6. **团队介绍**\n   - 核心成员\n   - 组织架构\n   - 人力资源\n\n7. **财务规划**\n   - 资金需求\n   - 财务预测\n   - 投资回报\n\n8. **风险分析**\n   - 市场风险\n   - 技术风险\n   - 应对策略\n\n创业项目：[项目简介]\n行业领域：[所属行业]\n融资需求：[资金需求和用途]"
    },
    {
        id: 108,
        title: "数据分析报告专家",
        category: "analysis",
        description: "制作专业、易懂的数据分析报告，提供决策支持",
        content: "你是一位专业的数据分析师，擅长将复杂的数据转化为清晰、易懂的分析报告，为企业决策提供支持。\n\n## 分析报告结构\n1. **报告摘要**\n   - 核心发现\n   - 关键指标\n   - 主要建议\n\n2. **数据概览**\n   - 数据来源\n   - 时间范围\n   - 样本规模\n\n3. **详细分析**\n   - 趋势分析\n   - 对比分析\n   - 相关性分析\n\n4. **可视化展示**\n   - 图表设计\n   - 数据解读\n   - 异常点说明\n\n5. **结论与建议**\n   - 主要结论\n   - 行动建议\n   - 预期效果\n\n分析主题：[业务问题]\n数据类型：[数据来源和类型]\n分析目标：[希望解决的问题或获得的洞察]"
    }
];

// 合并所有模板数据
const allTemplates = [...promptTemplates, ...highQualityTemplates];

// DOM元素
const templateGrid = document.getElementById('templateGrid');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const categoryButtons = document.querySelectorAll('.category-btn');
const loadMoreBtn = document.getElementById('loadMoreBtn');

// 当前选中的分类和显示数量
let currentCategory = 'all';
let displayedCount = 6; // 初始显示6个模板
const templatesPerPage = 6; // 每次加载6个模板

// 初始化页面
function init() {
    renderTemplates(allTemplates.slice(0, displayedCount));
    setupEventListeners();
}

// 设置事件监听器
function setupEventListeners() {
    // 搜索功能
    searchButton.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // 分类筛选
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 更新活动按钮状态
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 更新当前分类
            currentCategory = this.dataset.category;
            
            // 重置显示数量
            displayedCount = templatesPerPage;
            
            // 重新渲染模板
            filterTemplates();
        });
    });
    
    // 加载更多按钮
    loadMoreBtn.addEventListener('click', loadMoreTemplates);
}

// 处理搜索
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    if (searchTerm) {
        const filtered = allTemplates.filter(template => 
            template.title.toLowerCase().includes(searchTerm) ||
            template.description.toLowerCase().includes(searchTerm) ||
            template.content.toLowerCase().includes(searchTerm)
        );
        // 重置显示数量
        displayedCount = templatesPerPage;
        renderTemplates(filtered.slice(0, displayedCount));
    } else {
        filterTemplates();
    }
}

// 根据分类筛选模板
function filterTemplates() {
    if (currentCategory === 'all') {
        renderTemplates(allTemplates.slice(0, displayedCount));
    } else {
        const filtered = allTemplates.filter(template => 
            template.category === currentCategory
        );
        renderTemplates(filtered.slice(0, Math.min(displayedCount, filtered.length)));
    }
}

// 加载更多模板
function loadMoreTemplates() {
    displayedCount += templatesPerPage;
    filterTemplates();
    
    // 如果已经显示完所有模板，隐藏加载更多按钮
    const filteredTemplates = currentCategory === 'all' ? 
        allTemplates : 
        allTemplates.filter(template => template.category === currentCategory);
        
    if (displayedCount >= filteredTemplates.length) {
        loadMoreBtn.style.display = 'none';
    }
}

// 渲染模板卡片
function renderTemplates(templates) {
    templateGrid.innerHTML = '';
    
    if (templates.length === 0) {
        templateGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #666;">未找到匹配的模板</p>';
        loadMoreBtn.style.display = 'none';
        return;
    }
    
    templates.forEach(template => {
        const card = document.createElement('div');
        card.className = 'template-card';
        card.innerHTML = `
            <div class="template-header">
                <h3 class="template-title">${template.title}</h3>
                <span class="template-category">${getCategoryName(template.category)}</span>
            </div>
            <div class="template-content">
                <p class="template-description">${template.description}</p>
                <button class="copy-btn" data-content="${escapeHtml(template.content)}">复制提示词</button>
            </div>
        `;
        
        templateGrid.appendChild(card);
    });
    
    // 显示加载更多按钮
    loadMoreBtn.style.display = 'block';
    
    // 如果已经显示完所有模板，隐藏加载更多按钮
    const filteredTemplates = currentCategory === 'all' ? 
        allTemplates : 
        allTemplates.filter(template => template.category === currentCategory);
        
    if (displayedCount >= filteredTemplates.length) {
        loadMoreBtn.style.display = 'none';
    }
    
    // 为复制按钮添加事件监听器
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const content = this.dataset.content;
            copyToClipboard(unescapeHtml(content));
        });
    });
}

// 获取分类名称
function getCategoryName(categoryKey) {
    const categories = {
        'writing': '写作助手',
        'coding': '编程开发',
        'analysis': '分析研究',
        'creative': '创意生成',
        'business': '商业应用'
    };
    return categories[categoryKey] || categoryKey;
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // 显示成功消息
        const originalText = event.target.textContent;
        event.target.textContent = '已复制!';
        event.target.style.background = '#4CAF50';
        
        setTimeout(() => {
            event.target.textContent = originalText;
            event.target.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('复制失败: ', err);
        alert('复制失败，请手动选择复制');
    });
}

// HTML转义
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// HTML反转义
function unescapeHtml(safe) {
    return safe
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#039;/g, "'");
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);