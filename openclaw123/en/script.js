// ===== Resource Data (English) =====
const DATA = [
  {
    id: 'versions',
    icon: '🦞',
    name: 'OpenClaw Versions',
    desc: 'Recommended GUI versions — no command line needed',
    items: [
      {
        emoji: '🌐',
        name: 'OpenClaw Official',
        url: 'https://openclaw.ai/',
        desc: 'The original version with full features, requires command line knowledge',
        tag: 'Official'
      },
      {
        emoji: '🇨🇳',
        name: 'EasyClaw (China)',
        url: 'https://easyclaw.cn/',
        desc: 'By Fu Sheng, works in China, plug & play, perfect for beginners',
        tag: 'Recommended'
      },
      {
        emoji: '🎯',
        name: 'NetEase Youdao Lobster',
        url: 'https://lobsterai.youdao.com/#/index',
        desc: 'By NetEase Youdao, user-friendly Chinese interface',
        tag: 'China'
      },
      {
        emoji: '🐧',
        name: 'Tencent QClaw',
        url: 'https://claw.guanjia.qq.com/',
        desc: 'By Tencent PC Manager, already live and available',
        tag: 'China'
      }
    ]
  },
  {
    id: 'hubs',
    icon: '🏪',
    name: 'Hubs & Skill Marketplace',
    desc: 'Like an app store — discover and install various Skill plugins',
    items: [
      {
        emoji: '🏬',
        name: 'ClawHub Official',
        url: 'https://clawhub.ai/',
        desc: 'Official Skill marketplace, like an app store for OpenClaw',
        tag: 'Official'
      },
      {
        emoji: '📖',
        name: 'OpenClaw101',
        url: 'https://openclaw101.dev/zh',
        desc: 'Learning resource site, learn OpenClaw from scratch with detailed tutorials',
        tag: 'Tutorial'
      },
      {
        emoji: '🇨🇳',
        name: 'Skill Hub China',
        url: 'https://www.skill-cn.com/',
        desc: 'Chinese Skill aggregator with the most Chinese-language Skills',
        tag: 'China'
      },
      {
        emoji: '📑',
        name: 'OpenClaw: From Beginner to Pro Guide',
        url: 'https://my.feishu.cn/docx/P6zsdsgYco6i4XxLeIccvlpvnQe',
        desc: 'Comprehensive OpenClaw guide from beginner to expert, detailed Feishu doc tutorial',
        tag: 'Curated'
      }
    ]
  },
  {
    id: 'kol',
    icon: '📢',
    name: 'KOL · Influencers & Creators',
    desc: 'Follow these creators for the latest OpenClaw news and insights',
    items: [
      {
        emoji: '✍️',
        name: 'ChenLang AI',
        url: 'mailto:leogood@foxmail.com',
        desc: 'OpenClaw123 curator, sharing AI tool tips and insights',
        tag: 'Creator'
      },
      {
        emoji: '🦁',
        name: 'Fu Sheng',
        url: 'https://mp.weixin.qq.com/s/vAp5stHcQIAZvLZHRRXzYg',
        desc: 'CEO of Cheetah Mobile, creator of EasyClaw, sharing AI Agent & OpenClaw insights',
        tag: 'Industry Leader'
      },
      {
        emoji: '📝',
        name: 'Liu Xiaopai',
        url: 'https://mp.weixin.qq.com/s/H2DuoMR3Svoq_djWXAzA3Q',
        desc: 'Deep dives into the OpenClaw ecosystem on WeChat, full of insights',
        tag: 'Creator'
      },
      {
        emoji: '🎬',
        name: 'Andrej Karpathy: Deep Dive into LLMs like ChatGPT',
        url: 'https://www.bilibili.com/video/BV16cNEeXEer/',
        desc: 'Andrej Karpathy explains LLM fundamentals in depth — a must-watch for AI beginners',
        tag: 'Video'
      },
      {
        emoji: '📩',
        name: 'Submit / Collaborate',
        url: 'mailto:leogood@foxmail.com',
        desc: 'Want to list your resource? Email leogood@foxmail.com',
        tag: 'Contact Us'
      }
    ]
  },
  {
    id: 'reports',
    icon: '📊',
    name: 'Industry Reports & Insights',
    desc: 'Authoritative research reports on AI Agent and OpenClaw industry trends',
    items: [
      {
        emoji: '📋',
        name: 'AI Agent Industry Report (WeChat Deep Dive)',
        url: 'https://mp.weixin.qq.com/s/eGAzgZqJbbBjW34hGwe2bg',
        desc: 'In-depth analysis of the AI Agent industry landscape and trends',
        tag: 'Report'
      },
      {
        emoji: '📈',
        name: 'iiMedia: China AI Agent Industry Report',
        url: 'https://www.iimedia.cn/c400/110111.html',
        desc: 'Authoritative report by iiMedia Research on China\'s AI Agent market size and growth',
        tag: 'iiMedia'
      },
      {
        emoji: '🔍',
        name: 'Analysys: AI Agent Market Insights',
        url: 'https://www.analysys.cn/article/detail/20021171',
        desc: 'By Analysys, deep insights into the AI Agent market landscape and future direction',
        tag: 'Analysys'
      }
    ]
  },
  {
    id: 'future',
    icon: '🚀',
    name: 'Coming Soon · Stay Tuned',
    desc: 'Exciting things on the way — bookmark now so you don\'t miss out',
    items: [
      {
        emoji: '📱',
        name: 'Lei Jun\'s Lobster Phone',
        url: '#',
        desc: 'Xiaomi × OpenClaw deep collaboration, Lobster Phone coming soon',
        tag: 'Coming Soon'
      },
      {
        emoji: '💬',
        name: 'Aixin · "WeChat" for Agents',
        url: 'https://aixin.chat/',
        desc: 'Agent interoperability platform — letting AI Agents communicate and collaborate',
        tag: 'New Project'
      },
      {
        emoji: '🏠',
        name: 'HomeClaw Introduction',
        url: 'https://mp.weixin.qq.com/s/YkKCh5mOH-AR-Z23erDHFw',
        desc: 'Deep dive into HomeClaw — AI applications for the home',
        tag: 'Article'
      },
      {
        emoji: '🌐',
        name: 'When OpenClaw Takes Over the Internet',
        url: 'https://mp.weixin.qq.com/s/Vwqtw_lCNztE5dAI0c1jAQ',
        desc: 'Must-read article on how OpenClaw is reshaping the internet landscape',
        tag: 'Article'
      },
      {
        emoji: '🐦',
        name: 'OpenClaw Future Vision (Twitter)',
        url: 'https://x.com/runes_leo/status/2036468625171763599',
        desc: 'Deep discussion on the future direction of OpenClaw, worth following',
        tag: 'Tweet'
      },
      {
        emoji: '🌍',
        name: 'OpenClaw123.xyz',
        url: 'https://openclaw123.xyz',
        desc: 'Our official domain — stay tuned (under development)',
        tag: 'This Site'
      }
    ]
  }
];

// ===== Favorites (localStorage) =====
let favs = JSON.parse(localStorage.getItem('oc123_favs_en') || '{}');

function saveFavs() {
  localStorage.setItem('oc123_favs_en', JSON.stringify(favs));
}

// ===== Render =====
function render(data) {
  const main = document.getElementById('mainContent');
  const nav  = document.getElementById('topNav');
  main.innerHTML = '';
  nav.innerHTML  = '';

  let totalItems = 0;
  let totalCats  = data.length;

  data.forEach(cat => {
    totalItems += cat.items.length;

    // Nav anchor
    const a = document.createElement('a');
    a.href = '#' + cat.id;
    a.textContent = cat.icon + ' ' + cat.name;
    nav.appendChild(a);

    // Category section
    const section = document.createElement('section');
    section.className = 'category';
    section.id = cat.id;

    section.innerHTML = `
      <div class="category-header">
        <span class="cat-icon">${cat.icon}</span>
        <h2>${cat.name}</h2>
        <span class="cat-count">${cat.items.length} resources</span>
      </div>
      <div class="grid" id="grid-${cat.id}"></div>
    `;
    main.appendChild(section);

    const grid = section.querySelector('.grid');
    cat.items.forEach(item => {
      grid.appendChild(makeCard(item, cat.id));
    });
  });

  // Stats
  document.getElementById('heroStats').innerHTML = `
    <div class="stat"><b>${totalCats}</b> categories</div>
    <div class="stat"><b>${totalItems}</b> resources</div>
    <div class="stat"><b>${Object.keys(favs).length}</b> favorited</div>
  `;

  updateFabCount();
}

function makeCard(item, catId) {
  const key = catId + '::' + item.name;
  const isFav = !!favs[key];

  const wrapper = document.createElement('div');
  wrapper.style.display = 'contents';

  const isExternal = item.url.startsWith('http');
  const card = document.createElement(isExternal ? 'a' : 'div');
  card.className = 'card';
  if (isExternal) {
    card.href = item.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
  }

  card.innerHTML = `
    <button class="card-fav ${isFav ? 'active' : ''}" title="${isFav ? 'Remove' : 'Favorite'}" data-key="${key}">⭐</button>
    <div class="card-head">
      <span class="card-emoji">${item.emoji}</span>
      <span class="card-name">${item.name}</span>
    </div>
    <p class="card-desc">${item.desc}</p>
    ${item.tag ? `<span class="card-tag">${item.tag}</span>` : ''}
  `;

  card.querySelector('.card-fav').addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    const k = e.currentTarget.dataset.key;
    if (favs[k]) {
      delete favs[k];
      e.currentTarget.classList.remove('active');
      e.currentTarget.title = 'Favorite';
    } else {
      favs[k] = { ...item, catId };
      e.currentTarget.classList.add('active');
      e.currentTarget.title = 'Remove';
    }
    saveFavs();
    updateFabCount();
    renderDrawer();
    document.querySelector('#heroStats').querySelector('.stat:last-child b').textContent = Object.keys(favs).length;
  });

  return card;
}

// ===== Search =====
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

// ===== Favorites Drawer =====
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
    body.innerHTML = '<p class="empty-tip">No favorites yet. Click the ⭐ on any card to add!</p>';
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
        <button class="fi-del" data-key="${k}" title="Remove">✕</button>
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
      const cardFavBtn = document.querySelector(`.card-fav[data-key="${k}"]`);
      if (cardFavBtn) cardFavBtn.classList.remove('active');
      document.querySelector('#heroStats .stat:last-child b').textContent = Object.keys(favs).length;
    });
  });
}

function updateFabCount() {
  document.getElementById('fabCount').textContent = Object.keys(favs).length;
}

// ===== Init =====
render(DATA);
