
const tabsElement = document.getElementById('default-styled-tab');

const tabElements = [
    {
        id: 'profile',
        triggerEl: document.querySelector('#profile-styled-tab'),
        targetEl: document.querySelector('#styled-profile'),
    },
    {
        id: 'dashboard',
        triggerEl: document.querySelector('#dashboard-styled-tab'),
        targetEl: document.querySelector('#styled-dashboard'),
    },
    {
        id: 'settings',
        triggerEl: document.querySelector('#settings-styled-tab'),
        targetEl: document.querySelector('#styled-settings'),
    },
    {
        id: 'contacts',
        triggerEl: document.querySelector('#contacts-styled-tab'),
        targetEl: document.querySelector('#styled-contacts'),
    },
];

const options = {
    defaultTabId: 'profile', // tab mặc định hiển thị
    activeClasses: 'text-purple-600 border-b-4 border-purple-600',
    inactiveClasses: 'text-gray-500 border-b-2 border-gray-300 hover:text-purple-600 hover:border-purple-600',

    onShow: () => {
        console.log('Tab đã được mở');
    },
};

const tabs = new Tabs(tabsElement, tabElements, options);
