// ===== 资源数据 =====
const DATA = [
  {
    id: 'versions',
    icon: '🦞',
    name: 'OpenClaw 版本',
    desc: '推荐国内套壳界面操作版本，告别命令行',
    items: [
      {
        emoji: '🌐',
        name: 'OpenClaw 官方原版',
        url: 'https://openclaw.ai/',
        desc: '官方原版，功能最全，需要懂命令行操作',
        tag: '原版'
      },
      {
        emoji: '🇨🇳',
        name: 'EasyClaw 国内版',
        url: 'https://easyclaw.cn/',
        desc: '傅盛出品，国内可用，开箱即用，适合小白',
        tag: '推荐'
      },
      {
        emoji: '🎯',
        name: '网易有道龙虾',
        url: 'https://lobsterai.youdao.com/#/index',
        desc: '网易有道出品的龙虾版本，中文界面友好',
        tag: '国内版'
      },
      {
        emoji: '🐧',
        name: '腾讯 QClaw',
        url: 'https://claw.guanjia.qq.com/',
        desc: '腾讯电脑管家出品的 QClaw，已上线可用',
        tag: '国内版'
      }
    ]
  },
  {
    id: 'hubs',
    icon: '🏪',
    name: '聚合 & Skill 市场',
    desc: '类似应用商店，发现和安装各种 Skill 插件',
    items: [
      {
        emoji: '🏬',
        name: 'ClawHub 官方',
        url: 'https://clawhub.ai/',
        desc: '龙虾官方 Skill 市场，类似官方 APP 商店，应有尽有',
        tag: '官方'
      },
      {
        emoji: '📖',
        name: 'OpenClaw101',
        url: 'https://openclaw101.dev/zh',
        desc: '中文学习资源站，从零开始学 OpenClaw，教程详细',
        tag: '教程'
      },
      {
        emoji: '🇨🇳',
        name: 'Skill Hub 中国',
        url: 'https://www.skill-cn.com/',
        desc: '国内 Skill 聚合市场，中文 Skill 收录最全',
        tag: '国内'
      },
      {
        emoji: '📑',
        name: 'OpenClaw 从入门到精通指南',
        url: 'https://my.feishu.cn/docx/P6zsdsgYco6i4XxLeIccvlpvnQe',
        desc: 'OpenClaw 从入门到精通指南，飞书文档详细教程，零基础也能快速上手',
        tag: '精选'
      }
    ]
  },
  {
    id: 'kol',
    icon: '📢',
    name: 'KOL · 公众号 / 视频号 / 抖音',
    desc: '关注这些博主，第一时间获取 OpenClaw 最新资讯',
    items: [
      {
        emoji: '✍️',
        name: '陈朗AI',
        url: 'mailto:leogood@foxmail.com',
        desc: 'OpenClaw123 整理人，持续分享 AI 工具干货，联系投稿',
        tag: '博主'
      },
      {
        emoji: '🦁',
        name: '傅盛',
        url: 'https://mp.weixin.qq.com/s/vAp5stHcQIAZvLZHRRXzYg',
        desc: '猎豹移动CEO，EasyClaw出品人，深度分享AI Agent与OpenClaw实战经验',
        tag: '大佬'
      },
      {
        emoji: '📝',
        name: '刘小排',
        url: 'https://mp.weixin.qq.com/s/H2DuoMR3Svoq_djWXAzA3Q',
        desc: '公众号深度解读 OpenClaw 生态，干货满满值得关注',
        tag: '博主'
      },
      {
        emoji: '🎬',
        name: '安德烈·卡帕西：深入探索像ChatGPT这样的大语言模型',
        url: 'https://www.bilibili.com/video/BV16cNEeXEer/',
        desc: 'Andrej Karpathy 深入讲解大语言模型原理，B站1080P高清，AI入门必看',
        tag: '视频'
      },
      {
        emoji: '📩',
        name: '投稿 / 合作',
        url: 'mailto:leogood@foxmail.com',
        desc: '想发布你的资源？发邮件至 leogood@foxmail.com',
        tag: '联系我们'
      }
    ]
  },
  {
    id: 'reports',
    icon: '📊',
    name: '咨询报告 · 行业洞察',
    desc: '权威机构发布的 AI Agent 与 OpenClaw 行业研究报告',
    items: [
      {
        emoji: '📋',
        name: 'AI Agent 行业报告（微信深度解读）',
        url: 'https://mp.weixin.qq.com/s/eGAzgZqJbbBjW34hGwe2bg',
        desc: '深度解析 AI Agent 行业现状与趋势，干货满满的深度长文',
        tag: '报告'
      },
      {
        emoji: '📈',
        name: '艾媒咨询：中国AI Agent行业研究报告',
        url: 'https://www.iimedia.cn/c400/110111.html',
        desc: '艾媒咨询权威发布，全面分析中国 AI Agent 市场规模与发展趋势',
        tag: '艾媒咨询'
      },
      {
        emoji: '🔍',
        name: '易观分析：AI Agent市场洞察',
        url: 'https://www.analysys.cn/article/detail/20021171',
        desc: '易观分析出品，深入洞察 AI Agent 市场格局与未来走向',
        tag: '易观分析'
      }
    ]
  },
  {
    id: 'future',
    icon: '🚀',
    name: '未来规划 · 值得期待',
    desc: '正在路上的好东西，提前收藏不迷路',
    items: [
      {
        emoji: '📱',
        name: '雷军的龙虾手机',
        url: '#',
        desc: '小米 × OpenClaw 深度合作，龙虾手机即将到来，敬请期待',
        tag: '即将发布'
      },
      {
        emoji: '💬',
        name: '爱信 Aixin · Agent的"微信"',
        url: 'https://aixin.chat/',
        desc: 'Agent 互联互通平台，让 AI Agent 之间可以互相通讯和协作',
        tag: '新项目'
      },
      {
        emoji: '🏠',
        name: 'HomeClaw 介绍',
        url: 'https://mp.weixin.qq.com/s/YkKCh5mOH-AR-Z23erDHFw',
        desc: 'HomeClaw 深度介绍，了解家庭场景下的 AI 应用新方向',
        tag: '文章'
      },
      {
        emoji: '🌐',
        name: '当 OpenClaw 接管互联网',
        url: 'https://mp.weixin.qq.com/s/Vwqtw_lCNztE5dAI0c1jAQ',
        desc: '深度好文，OpenClaw 如何改变互联网格局，必读',
        tag: '文章'
      },
      {
        emoji: '🐦',
        name: 'OpenClaw 未来展望（Twitter）',
        url: 'https://x.com/runes_leo/status/2036468625171763599',
        desc: '关于 OpenClaw 未来发展方向的深度探讨，值得关注',
        tag: '推文'
      },
      {
        emoji: '🌍',
        name: 'OpenClaw123.xyz',
        url: 'https://openclaw123.xyz',
        desc: '本站官方域名，即将上线，敬请期待（研发中）',
        tag: '本站'
      }
    ]
  }
];

// ===== 收藏（localStorage） =====
let favs = JSON.parse(localStorage.getItem('oc123_favs') || '{}');

function saveFavs() {
  localStorage.setItem('oc123_favs', JSON.stringify(favs));
}

// ===== 渲染 =====
function render(data) {
  const main = document.getElementById('mainContent');
  const nav  = document.getElementById('topNav');
  main.innerHTML = '';
  nav.innerHTML  = '';

  let totalItems = 0;
  let totalCats  = data.length;

  data.forEach(cat => {
    totalItems += cat.items.length;

    // 导航锚点
    const a = document.createElement('a');
    a.href = '#' + cat.id;
    a.textContent = cat.icon + ' ' + cat.name;
    nav.appendChild(a);

    // 分类区块
    const section = document.createElement('section');
    section.className = 'category';
    section.id = cat.id;

    section.innerHTML = `
      <div class="category-header">
        <span class="cat-icon">${cat.icon}</span>
        <h2>${cat.name}</h2>
        <span class="cat-count">${cat.items.length} 个资源</span>
      </div>
      <div class="grid" id="grid-${cat.id}"></div>
    `;
    main.appendChild(section);

    const grid = section.querySelector('.grid');
    cat.items.forEach(item => {
      grid.appendChild(makeCard(item, cat.id));
    });
  });

  // 统计栏
  document.getElementById('heroStats').innerHTML = `
    <div class="stat"><b>${totalCats}</b> 个分类</div>
    <div class="stat"><b>${totalItems}</b> 个资源</div>
    <div class="stat"><b>${Object.keys(favs).length}</b> 已收藏</div>
  `;

  updateFabCount();
}

function makeCard(item, catId) {
  const key = catId + '::' + item.name;
  const isFav = !!favs[key];

  const wrapper = document.createElement('div');
  wrapper.style.display = 'contents';

  // 如果链接是 # 或 mailto，不用 <a> 包裹外层跳转
  const isExternal = item.url.startsWith('http');
  const card = document.createElement(isExternal ? 'a' : 'div');
  card.className = 'card';
  if (isExternal) {
    card.href = item.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
  }

  card.innerHTML = `
    <button class="card-fav ${isFav ? 'active' : ''}" title="${isFav ? '取消收藏' : '收藏'}" data-key="${key}">⭐</button>
    <div class="card-head">
      <span class="card-emoji">${item.emoji}</span>
      <span class="card-name">${item.name}</span>
    </div>
    <p class="card-desc">${item.desc}</p>
    ${item.tag ? `<span class="card-tag">${item.tag}</span>` : ''}
  `;

  // 收藏按钮点击
  card.querySelector('.card-fav').addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    const k = e.currentTarget.dataset.key;
    if (favs[k]) {
      delete favs[k];
      e.currentTarget.classList.remove('active');
      e.currentTarget.title = '收藏';
    } else {
      favs[k] = { ...item, catId };
      e.currentTarget.classList.add('active');
      e.currentTarget.title = '取消收藏';
    }
    saveFavs();
    updateFabCount();
    renderDrawer();
    // 刷新统计
    document.querySelector('#heroStats').querySelector('.stat:last-child b').textContent = Object.keys(favs).length;
  });

  return card;
}

// ===== 搜索 =====
function filterCards() {
  const q = document.getElementById('searchInput').value.trim().toLowerCase();
  if (!q) {
    render(DATA);
    document.getElementById('noResult').style.display = 'none';
    return;
  }

  const filtered = DATA.map(cat => ({
    ...cat,
    items: cat.items.filter(item =>
      item.name.toLowerCase().includes(q) ||
      item.desc.toLowerCase().includes(q) ||
      (item.tag && item.tag.toLowerCase().includes(q))
    )
  })).filter(cat => cat.items.length > 0);

  if (filtered.length === 0) {
    document.getElementById('mainContent').innerHTML = '';
    document.getElementById('noResult').style.display = 'block';
  } else {
    document.getElementById('noResult').style.display = 'none';
    render(filtered);
  }
}

function clearSearch() {
  document.getElementById('searchInput').value = '';
  filterCards();
}

// ===== 收藏抽屉 =====
function toggleFav() {
  const drawer  = document.getElementById('drawer');
  const overlay = document.getElementById('drawerOverlay');
  const isOpen  = drawer.classList.contains('open');
  if (isOpen) {
    drawer.classList.remove('open');
    overlay.classList.remove('open');
  } else {
    renderDrawer();
    drawer.classList.add('open');
    overlay.classList.add('open');
  }
}

function renderDrawer() {
  const body = document.getElementById('drawerBody');
  const keys = Object.keys(favs);
  if (keys.length === 0) {
    body.innerHTML = '<p class="empty-tip">还没有收藏，点击卡片右上角的 ⭐ 添加吧！</p>';
    return;
  }
  body.innerHTML = keys.map(k => {
    const it = favs[k];
    return `
      <a class="fav-item" href="${it.url}" target="_blank" rel="noopener noreferrer">
        <span class="fi-emoji">${it.emoji}</span>
        <div class="fi-info">
          <div class="fi-name">${it.name}</div>
          <div class="fi-desc">${it.desc}</div>
        </div>
        <button class="fi-del" data-key="${k}" title="移除收藏">✕</button>
      </a>
    `;
  }).join('');

  body.querySelectorAll('.fi-del').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      const k = btn.dataset.key;
      delete favs[k];
      saveFavs();
      updateFabCount();
      renderDrawer();
      // 更新卡片上的收藏按钮状态
      const cardFavBtn = document.querySelector(`.card-fav[data-key="${k}"]`);
      if (cardFavBtn) cardFavBtn.classList.remove('active');
      document.querySelector('#heroStats .stat:last-child b').textContent = Object.keys(favs).length;
    });
  });
}

function updateFabCount() {
  document.getElementById('fabCount').textContent = Object.keys(favs).length;
}

// ===== 初始化 =====
render(DATA);
