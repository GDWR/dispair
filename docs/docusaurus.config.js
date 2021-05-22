/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: 'Dispair',
    tagline: 'A webhook client for Discord Interactions.',
    url: 'https://gdwr.github.io/dispair/',
    baseUrl: '/',
    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',
    favicon: 'img/favicon.ico',
    organizationName: 'GDWR', // Usually your GitHub org/user name.
    projectName: 'dispair', // Usually your repo name.
    themeConfig: {
        navbar: {
            title: 'Dispair',
            logo: {
                alt: 'My Site Logo',
                src: 'img/logo.svg',
            },
            items: [
                {
                    type: 'doc',
                    docId: 'getting-started',
                    position: 'left',
                    label: 'Tutorial',
                },
                {
                    href: 'https://github.com/GDWR/dispair',
                    label: 'GitHub',
                    position: 'right',
                },
            ],
        },
        footer: {
            style: 'dark',
            links: [
                {
                    title: 'Docs',
                    items: [
                        {
                            label: 'Tutorial',
                            to: '/pages/getting-started',
                        },
                    ],
                },
                {
                    title: 'Community',
                    items: [],
                },
                {
                    title: 'More',
                    items: [
                        {
                            label: 'GitHub',
                            href: 'https://github.com/GDWR/dispair',
                        },
                    ],
                },
            ],
            copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
        },
    },
    presets: [
        [
            '@docusaurus/preset-classic',
            {
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                    // Please change this to your repo.
                    editUrl:
                        'https://github.com/GDWR/dispair/edit/master/website',
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            },
        ],
    ],
}
