document.addEventListener("DOMContentLoaded", () => {

    const footerData = window.footerData || {};

    const {
        isAuthenticated,
        userRole,
        urls
    } = footerData;

    /* =========================
       SOCIAL LINKS
    ========================= */

    const socials = [
        { icon: "facebook-f", url: "#" },
        { icon: "twitter", url: "#" },
        { icon: "instagram", url: "#" },
        { icon: "linkedin-in", url: "#" },
        { icon: "youtube", url: "#" }
    ];

    document.getElementById("social-links").innerHTML =
        socials.map(s => `
            <a href="${s.url}"
               class="group w-14 h-14 bg-gray-900 border border-gray-800 rounded-2xl flex items-center justify-center hover:-translate-y-2 transition-all duration-300">
                <i class="fab fa-${s.icon} text-gray-400 group-hover:text-white"></i>
            </a>
        `).join('');

    /* =========================
       QUICK LINKS
    ========================= */

    const quickLinks = [
        {
            name: "Home",
            icon: "home",
            url: urls.home
        },
        {
            name: "About",
            icon: "info-circle",
            url: urls.about
        },
        {
            name: "Contact",
            icon: "envelope",
            url: urls.contact
        }
    ];

    if (isAuthenticated) {

        switch (userRole) {

            case "admin":
                quickLinks.push({
                    name: "Admin Panel",
                    icon: "user-shield",
                    url: urls.adminPanel
                });
                break;

            case "manager":
                quickLinks.push(
                    {
                        name: "Analytics",
                        icon: "chart-pie",
                        url: urls.analyticsDashboard
                    },
                    {
                        name: "Dashboard",
                        icon: "chart-line",
                        url: urls.cattleDashboard
                    }
                );
                break;

            case "author":
                quickLinks.push(
                    {
                        name: "Articles",
                        icon: "newspaper",
                        url: urls.articles
                    },
                    {
                        name: "Write Article",
                        icon: "pen-nib",
                        url: urls.createArticle
                    }
                );
                break;

            case "cattle_manager":
                quickLinks.push(
                    {
                        name: "Cattle Dashboard",
                        icon: "tractor",
                        url: urls.cattleDashboard
                    },
                    {
                        name: "Add Cattle",
                        icon: "plus-circle",
                        url: urls.addCattle
                    }
                );
                break;

            case "farmer":
                quickLinks.push({
                    name: "My Herd",
                    icon: "people-carry",
                    url: urls.cattleDashboard
                });
                break;
        }

    } else {

        quickLinks.push(
            {
                name: "Login",
                icon: "sign-in-alt",
                url: urls.login
            },
            {
                name: "Signup",
                icon: "user-plus",
                url: urls.signup
            }
        );
    }

    document.getElementById("quick-links").innerHTML =
        quickLinks.map(link => `
            <li>
                <a href="${link.url}" class="group flex items-center gap-3 text-gray-400 hover:text-green-400">
                    <div class="w-8 h-8 bg-gray-900 rounded-xl flex items-center justify-center">
                        <i class="fas fa-${link.icon} text-sm"></i>
                    </div>
                    <span>${link.name}</span>
                </a>
            </li>
        `).join('');

    /* =========================
       TOOLS
    ========================= */

    let tools = [];

    const roleTools = {
        admin: [
            {
                name: "Analytics",
                icon: "chart-pie",
                url: urls.analyticsDashboard
            },
            {
                name: "Devices",
                icon: "microchip",
                url: urls.deviceDiagnostics
            },
            {
                name: "Profile",
                icon: "user",
                url: urls.profile
            }
        ],

        manager: [
            {
                name: "Analytics",
                icon: "chart-pie",
                url: urls.analyticsDashboard
            },
            {
                name: "Dashboard",
                icon: "chart-line",
                url: urls.cattleDashboard
            }
        ],

        author: [
            {
                name: "Articles",
                icon: "newspaper",
                url: urls.articles
            },
            {
                name: "Write Article",
                icon: "pen-nib",
                url: urls.createArticle
            }
        ],

        cattle_manager: [
            {
                name: "Cattle Dashboard",
                icon: "tractor",
                url: urls.cattleDashboard
            },
            {
                name: "Add Cattle",
                icon: "plus-circle",
                url: urls.addCattle
            }
        ],

        farmer: [
            {
                name: "My Herd",
                icon: "people-carry",
                url: urls.cattleDashboard
            }
        ]
    };

    if (isAuthenticated) {
        tools = roleTools[userRole] || [];
    } else {
        tools = [
            {
                name: "Articles",
                icon: "newspaper",
                url: urls.articles
            },
            {
                name: "Login",
                icon: "sign-in-alt",
                url: urls.login
            }
        ];
    }

    document.getElementById("tools-links").innerHTML =
        tools.map(tool => `
            <li>
                <a href="${tool.url}" class="group flex items-center gap-3 text-gray-400">
                    <div class="w-8 h-8 bg-gray-900 rounded-xl flex items-center justify-center">
                        <i class="fas fa-${tool.icon} text-sm"></i>
                    </div>
                    <span>${tool.name}</span>
                </a>
            </li>
        `).join('');

    /* =========================
       CONTACT
    ========================= */

    const contacts = [
        {
            icon: "envelope",
            title: "Email",
            line1: "info@cattlecare.com",
            line2: "support@cattlecare.com"
        },
        {
            icon: "phone",
            title: "Phone",
            line1: "+91 98765 43210",
            line2: "Mon - Sat • 9AM - 6PM"
        },
        {
            icon: "map-marker-alt",
            title: "Location",
            line1: "Pune, Maharashtra",
            line2: "India"
        }
    ];

    document.getElementById("contact-items").innerHTML =
        contacts.map(c => `
            <div class="flex items-start gap-4">
                <div class="w-12 h-12 bg-gradient-to-r from-green-400 to-blue-500 rounded-2xl flex items-center justify-center">
                    <i class="fas fa-${c.icon} text-white"></i>
                </div>
                <div>
                    <h4 class="font-semibold">${c.title}</h4>
                    <p class="text-gray-400 text-sm">${c.line1}</p>
                    <p class="text-gray-500 text-xs">${c.line2}</p>
                </div>
            </div>
        `).join('');
});