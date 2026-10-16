# -*- coding: utf-8 -*-
"""
Main Builder Script for AC Repair Naples Fl Blog System
1. Combines articles from blog_data_1, blog_data_2, blog_data_3
2. Generates root blog.html
3. Generates blog/index.html
4. Generates 10 individual article HTML pages in blog/
5. Updates _redirects, vercel.json, and sitemap.xml
"""

import os
import glob
import json
import re

from blog_data_1 import ARTICLES_PART_1
from blog_data_2 import ARTICLES_PART_2
from blog_data_3 import ARTICLES_PART_3

ALL_ARTICLES = ARTICLES_PART_1 + ARTICLES_PART_2 + ARTICLES_PART_3
print(f"Total articles loaded: {len(ALL_ARTICLES)}")

def get_desktop_nav(depth=0):
    p = "../" if depth == 1 else ""
    return f"""      <nav aria-label="Main Navigation" class="desktop-nav">
        <a href="{p}index.html" class="nav-link">Home</a>
        <a href="{p}about.html" class="nav-link">About</a>
        <div class="nav-dropdown">
          <a href="{p}services.html" class="nav-link" aria-haspopup="true">
            Services
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 9l6 6 6-6"/></svg>
          </a>
          <div class="nav-dropdown-menu" role="menu">
            <a href="{p}ac-not-cooling.html" class="nav-dropdown-item" role="menuitem">
              <span class="nav-dropdown-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg>
              </span>
              <div>
                <span class="nav-dropdown-title">AC Repair &amp; Diagnostics</span>
                <span class="nav-dropdown-desc">Rapid diagnosis for warm air, frozen coils, clogs, and leaks.</span>
              </div>
            </a>
            <a href="{p}ac-maintenance-tune-up.html" class="nav-dropdown-item" role="menuitem">
              <span class="nav-dropdown-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
              </span>
              <div>
                <span class="nav-dropdown-title">Seasonal Maintenance Tune-Up</span>
                <span class="nav-dropdown-desc">24-point coastal HVAC inspection &amp; coil sanitization.</span>
              </div>
            </a>
            <a href="{p}hvac-system-replacement.html" class="nav-dropdown-item" role="menuitem">
              <span class="nav-dropdown-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              </span>
              <div>
                <span class="nav-dropdown-title">HVAC System Replacement</span>
                <span class="nav-dropdown-desc">High-efficiency variable-speed heat pump installations.</span>
              </div>
            </a>
            <div style="padding-top:0.6rem;margin-top:0.4rem;border-top:1px solid #f1f5f9;">
              <a href="{p}services.html" style="font-size:0.85rem;color:#0284c7;font-weight:600;text-decoration:none;">
                View All HVAC Services &rarr;
              </a>
            </div>
          </div>
        </div>
        <a href="{p}locations.html" class="nav-link">Service Areas</a>
        <a href="{p}blog.html" class="nav-link active">Blog</a>
        <a href="{p}contact.html" class="nav-link">Contact</a>
      </nav>"""

def get_mobile_drawer(depth=0):
    p = "../" if depth == 1 else ""
    return f"""    <div id="mobileDrawer" class="mobile-drawer" aria-hidden="true">
      <div class="mobile-drawer-inner">
        <div class="mobile-drawer-links">
          <a href="{p}index.html" class="mobile-nav-link">Home</a>
          <a href="{p}about.html" class="mobile-nav-link">About Us</a>
          <a href="{p}services.html" class="mobile-nav-link">Services Hub</a>
          <div style="padding-left:1rem;display:flex;flex-direction:column;gap:0.4rem;">
            <a href="{p}ac-not-cooling.html" style="color:#94a3b8;font-size:0.9rem;text-decoration:none;">&bull; AC Repair &amp; Diagnostics</a>
            <a href="{p}ac-maintenance-tune-up.html" style="color:#94a3b8;font-size:0.9rem;text-decoration:none;">&bull; Seasonal Maintenance</a>
            <a href="{p}hvac-system-replacement.html" style="color:#94a3b8;font-size:0.9rem;text-decoration:none;">&bull; System Replacement</a>
          </div>
          <a href="{p}locations.html" class="mobile-nav-link">Service Areas</a>
          <a href="{p}blog.html" class="mobile-nav-link active">Blog &amp; Advice</a>
          <a href="{p}contact.html" class="mobile-nav-link">Contact</a>
        </div>
        <div style="margin-top:1.5rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.1);">
          <a href="tel:+12396861066" class="btn btn-primary" style="width:100%;text-align:center;">
            Call (239) 686-1066
          </a>
        </div>
      </div>
    </div>"""

def get_header(depth=0):
    p = "../" if depth == 1 else ""
    return f"""  <!-- Top Announcement Bar -->
  <div class="top-bar">
    <div class="site-container top-bar-inner">
      <div class="top-bar-badge">
        <span class="status-dot"></span>
        <span>24/7 Emergency AC Service in Naples, FL &bull; Fast Dispatch</span>
      </div>
      <div class="top-bar-links">
        <span class="top-bar-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
          4389 Enterprise Ave, Naples, FL
        </span>
        <a href="tel:+12396861066" class="top-bar-link top-bar-phone">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
          (239) 686-1066
        </a>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header class="site-header">
    <div class="site-container site-header-inner">
      <a href="{p}index.html" class="site-logo" aria-label="Premium AC Solutions Home">
        <img src="{p}assets/images/logo.svg" alt="Premium AC Solutions Logo" width="220" height="48" />
      </a>

{get_desktop_nav(depth)}

      <div class="nav-cta-group">
        <a href="tel:+12396861066" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
          <span>(239) 686-1066</span>
        </a>
        <button id="mobileNavToggle" class="mobile-nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobileDrawer">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
    </div>

{get_mobile_drawer(depth)}
  </header>"""

def get_footer(depth=0):
    p = "../" if depth == 1 else ""
    return f"""  <!-- Footer -->
  <footer class="site-footer">
    <div class="site-container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="{p}index.html" class="footer-logo" aria-label="Premium AC Solutions Home">
            <img src="{p}assets/images/logo-white.svg" alt="Premium AC Solutions Logo" width="220" height="48" />
          </a>
          <p class="footer-desc">
            Premium AC Solutions delivers reliable air conditioning repair, precision seasonal tune-ups, and high-efficiency HVAC replacements across Naples and Collier County, FL.
          </p>
          <div style="display:flex;gap:0.75rem;align-items:center;color:#38bdf8;font-size:0.85rem;font-weight:600;">
            <span>EPA Certified</span> &bull;
            <span>Licensed &amp; Insured</span> &bull;
            <span>Same-Day Dispatch</span>
          </div>
        </div>

        <div class="footer-col">
          <h3>Core Services</h3>
          <ul class="footer-nav-list">
            <li><a href="{p}ac-not-cooling.html" class="footer-nav-link">Emergency AC Repair</a></li>
            <li><a href="{p}ac-maintenance-tune-up.html" class="footer-nav-link">AC Maintenance &amp; Tune-Up</a></li>
            <li><a href="{p}hvac-system-replacement.html" class="footer-nav-link">HVAC System Replacement</a></li>
            <li><a href="{p}services.html" class="footer-nav-link">All HVAC Services</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Service Areas</h3>
          <ul class="footer-nav-list">
            <li><a href="{p}locations.html" class="footer-nav-link">Naples, FL</a></li>
            <li><a href="{p}locations.html" class="footer-nav-link">North Naples</a></li>
            <li><a href="{p}locations.html" class="footer-nav-link">East Naples</a></li>
            <li><a href="{p}locations.html" class="footer-nav-link">Park Shore &amp; Port Royal</a></li>
            <li><a href="{p}locations.html" class="footer-nav-link">Collier County Coverage</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h3>Contact Details</h3>
          <div class="footer-contact-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
            <div>
              <a href="tel:+12396861066">(239) 686-1066</a>
              <div style="font-size:0.8rem;color:#94a3b8;">24/7 Emergency Line</div>
            </div>
          </div>
          <div class="footer-contact-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <div>
              <p style="margin:0;color:#cbd5e1;">4389 Enterprise Avenue</p>
              <p style="margin:0;color:#cbd5e1;">Naples, FL 34104</p>
            </div>
          </div>
          <div class="footer-contact-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div>
              <p style="margin:0;color:#cbd5e1;">Mon–Fri: 7:00 AM – 7:00 PM</p>
              <p style="margin:0;color:#cbd5e1;">Sat: 8:00 AM – 4:00 PM</p>
              <p style="margin:0;color:#38bdf8;font-weight:600;">24/7 Emergency Available</p>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>
          &copy; 2026 Premium AC Solutions. All rights reserved.
        </div>
        <div class="footer-bottom-links">
          <a href="{p}about.html">About</a>
          <a href="{p}services.html">Services</a>
          <a href="{p}locations.html">Service Areas</a>
          <a href="{p}blog.html">Blog</a>
          <a href="{p}contact.html">Contact</a>
          <a href="{p}privacy-policy.html">Privacy Policy</a>
          <a href="{p}sitemap.xml">Sitemap</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Mobile Sticky CTA Bar -->
  <div class="mobile-sticky-cta" role="region" aria-label="Quick mobile action">
    <div class="mobile-sticky-cta-inner">
      <a href="tel:+12396861066" class="btn btn-primary" style="padding:0.75rem 1rem;font-size:0.92rem;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
        <span>Call (239) 686-1066</span>
      </a>
      <a href="{p}contact.html" class="btn btn-outline" style="padding:0.75rem 0.85rem;font-size:0.9rem;">
        <span>Book Online</span>
      </a>
    </div>
  </div>

  <script src="{p}assets/js/main.js"></script>"""

def render_trust_strip():
    return """<section class="trust-strip" aria-label="Company Credentials">
  <div class="site-container">
    <div class="trust-grid">
      <div class="trust-item">
        <span class="trust-item-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </span>
        <div class="trust-item-text">
          <span class="trust-item-label">Licensed &amp; Insured</span>
          <span class="trust-item-sub">Collier County Compliant</span>
        </div>
      </div>
      <div class="trust-item">
        <span class="trust-item-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </span>
        <div class="trust-item-text">
          <span class="trust-item-label">EPA Certified</span>
          <span class="trust-item-sub">Universal Section 608</span>
        </div>
      </div>
      <div class="trust-item">
        <span class="trust-item-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </span>
        <div class="trust-item-text">
          <span class="trust-item-label">24/7 Emergency Line</span>
          <span class="trust-item-sub">Same-Day Dispatch</span>
        </div>
      </div>
      <div class="trust-item">
        <span class="trust-item-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </span>
        <div class="trust-item-text">
          <span class="trust-item-label">Written Warranties</span>
          <span class="trust-item-sub">100% Workmanship Backed</span>
        </div>
      </div>
    </div>
  </div>
</section>"""

def render_blog_listing_html(depth=0):
    p = "../" if depth == 1 else ""
    card_link_prefix = "" if depth == 1 else "blog/"
    
    cards_html = []
    for art in ALL_ARTICLES:
        card = f"""      <article class="service-card" style="display:flex;flex-direction:column;height:100%;overflow:hidden;padding:0;">
        <div style="position:relative;height:220px;overflow:hidden;background:#0f2438;">
          <a href="{card_link_prefix}{art['slug']}.html" tabindex="-1" aria-hidden="true">
            <img src="{p}{art['image']}" alt="{art['image_alt']}" style="width:100%;height:100%;object-fit:cover;transition:transform 0.3s ease;" loading="lazy" />
          </a>
          <span style="position:absolute;top:12px;left:12px;z-index:2;">
            <span style="background:#0284c7;color:#fff;font-size:0.75rem;font-weight:700;padding:4px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.04em;">{art['category']}</span>
          </span>
        </div>
        <div style="padding:1.5rem;display:flex;flex-direction:column;flex:1 1 auto;">
          <div style="display:flex;align-items:center;gap:0.5rem;color:#64748b;font-size:0.82rem;margin-bottom:0.6rem;">
            <span>{art['date']}</span>
            <span>&bull;</span>
            <span>{art['read_time']}</span>
          </div>
          <h2 style="font-size:1.18rem;font-weight:700;line-height:1.35;margin:0 0 0.65rem;">
            <a href="{card_link_prefix}{art['slug']}.html" style="color:#0f2438;text-decoration:none;">{art['title']}</a>
          </h2>
          <p style="color:#64748b;font-size:0.92rem;line-height:1.6;margin:0 0 1.25rem;flex:1 1 auto;">{art['excerpt']}</p>
          <div style="padding-top:0.85rem;border-top:1px solid #f1f5f9;">
            <a href="{card_link_prefix}{art['slug']}.html" style="color:#0284c7;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:0.4rem;font-size:0.92rem;">
              Read Guide <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
          </div>
        </div>
      </article>"""
        cards_html.append(card)
    
    cards_joined = "\n".join(cards_html)
    
    # JSON-LD Schema
    blog_schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": "https://acrepairnaplesfl-vercel.vercel.app/blog#blog",
        "name": "Premium AC Solutions Knowledge Hub & Blog",
        "description": "Expert air conditioning repair guides, troubleshooting advice, and seasonal cooling tips from licensed technicians in Naples, Florida.",
        "url": "https://acrepairnaplesfl-vercel.vercel.app/blog",
        "publisher": {
            "@type": "HVACBusiness",
            "@id": "https://acrepairnaplesfl-vercel.vercel.app/#localbusiness",
            "name": "Premium AC Solutions",
            "telephone": "+12396861066",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "4389 Enterprise Avenue",
                "addressLocality": "Naples",
                "addressRegion": "FL",
                "postalCode": "34104",
                "addressCountry": "US"
            }
        },
        "blogPost": [
            {
                "@type": "BlogPosting",
                "headline": a["title"],
                "url": f"https://acrepairnaplesfl-vercel.vercel.app/blog/{a['slug']}",
                "datePublished": a["date_iso"],
                "description": a["excerpt"]
            } for a in ALL_ARTICLES
        ]
    }
    
    schema_json_str = json.dumps(blog_schema, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">

<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-684T43FDEM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-684T43FDEM');
  </script>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="6yi7cacoszw7clEa9mq7gAq4vWRYRv0KIjPzy5me_Tg" />
  <title>HVAC &amp; AC Repair Blog Naples FL | Expert Homeowner Guides</title>
  <meta name="description"
    content="Practical air conditioning troubleshooting guides, energy-saving tips, and HVAC maintenance advice from licensed cooling technicians in Naples, Florida.">
  <meta name="author" content="Premium AC Solutions">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://acrepairnaplesfl-vercel.vercel.app/blog">

  <meta property="og:type" content="website">
  <meta property="og:title" content="HVAC &amp; AC Repair Blog Naples FL | Expert Homeowner Guides">
  <meta property="og:description"
    content="Practical air conditioning troubleshooting guides, energy-saving tips, and HVAC maintenance advice from licensed cooling technicians in Naples, Florida.">
  <meta property="og:url" content="https://acrepairnaplesfl-vercel.vercel.app/blog">
  <meta property="og:image" content="{p}assets/images/services/ac-not-cooling.webp">

  <link rel="icon" type="image/svg+xml" href="{p}assets/images/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="{p}assets/images/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="{p}assets/images/favicon-16x16.png" />
  <link rel="shortcut icon" href="{p}assets/images/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="{p}assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="{p}site.webmanifest" />
  <link rel="stylesheet" href="{p}assets/global.css" />

  <script type="application/ld+json">
{schema_json_str}
  </script>
</head>

<body>
{get_header(depth)}

  <main id="main-content">
    <!-- Breadcrumbs -->
    <div class="site-container breadcrumbs" aria-label="Breadcrumb">
      <a href="{p}index.html">Home</a>
      <span class="breadcrumb-separator">/</span>
      <span aria-current="page">Blog &amp; Knowledge Hub</span>
    </div>

    <!-- Hero Section -->
    <section class="page-hero">
      <div class="site-container">
        <div style="max-width:800px;margin:0 auto;text-align:center;">
          <div class="section-tag" style="background:rgba(2,132,199,0.15);color:#38bdf8;">Homeowner Cooling Advice</div>
          <h1 class="page-hero-title">
            Naples AC Repair &amp; HVAC Knowledge Hub
          </h1>
          <p class="page-hero-subtitle">
            Expert cooling advice, step-by-step troubleshooting guides, and seasonal maintenance wisdom written by EPA-certified HVAC professionals serving homeowners across Naples, FL.
          </p>
        </div>
      </div>
    </section>

{render_trust_strip()}

    <!-- Blog Grid Section -->
    <section class="section">
      <div class="site-container">
        <div class="section-header">
          <div class="section-tag">All 10 Guides</div>
          <h2 class="section-title">Latest HVAC Troubleshooting &amp; Maintenance Guides</h2>
          <p class="section-subtitle">
            Browse our original articles addressing the most frequent air conditioning, drainage, and mechanical issues in Collier County residences.
          </p>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(320px, 1fr));gap:2rem;">
{cards_joined}
        </div>
      </div>
    </section>

    <!-- Bottom CTA Banner -->
    <section class="cta-banner">
      <div class="site-container">
        <div class="cta-banner-inner">
          <div style="max-width:680px;">
            <h2 class="cta-banner-title">Need Immediate Air Conditioning Assistance in Naples?</h2>
            <p class="cta-banner-desc">
              Whether your system stopped blowing cold air, has frozen coils, or is overdue for a precision seasonal tune-up, our certified technicians are on call 24/7.
            </p>
          </div>
          <div class="cta-banner-actions">
            <a href="tel:+12396861066" class="btn btn-primary" style="background:#fff;color:#0f2438;font-weight:700;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
              <span>Call (239) 686-1066</span>
            </a>
            <a href="{p}contact.html" class="btn btn-outline" style="border-color:#fff;color:#fff;">
              <span>Request Service Online</span>
            </a>
          </div>
        </div>
      </div>
    </section>
  </main>

{get_footer(depth)}
</body>

</html>"""

def render_article_page_html(art):
    slug = art['slug']
    related = [a for a in ALL_ARTICLES if a['slug'] != slug][:3]
    
    related_cards = []
    for r in related:
        card = f"""        <article class="service-card" style="display:flex;flex-direction:column;padding:0;overflow:hidden;">
          <div style="height:180px;background:#0f2438;overflow:hidden;">
            <a href="{r['slug']}.html" tabindex="-1">
              <img src="../{r['image']}" alt="{r['image_alt']}" style="width:100%;height:100%;object-fit:cover;" loading="lazy" />
            </a>
          </div>
          <div style="padding:1.25rem;display:flex;flex-direction:column;flex:1 1 auto;">
            <div style="color:#64748b;font-size:0.8rem;margin-bottom:0.4rem;">{r['date']} &bull; {r['read_time']}</div>
            <h3 style="font-size:1.05rem;line-height:1.35;margin:0 0 0.5rem;">
              <a href="{r['slug']}.html" style="color:#0f2438;text-decoration:none;">{r['title']}</a>
            </h3>
            <p style="color:#64748b;font-size:0.88rem;line-height:1.5;margin:0 0 1rem;flex:1 1 auto;">{r['excerpt']}</p>
            <a href="{r['slug']}.html" style="color:#0284c7;font-weight:700;font-size:0.88rem;text-decoration:none;">
              Read Guide &rarr;
            </a>
          </div>
        </article>"""
        related_cards.append(card)
    related_joined = "\n".join(related_cards)

    # Article Schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": f"https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}#article",
        "headline": art["title"],
        "description": art["meta_desc"],
        "url": f"https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}",
        "datePublished": art["date_iso"],
        "dateModified": art["date_iso"],
        "image": f"https://acrepairnaplesfl-vercel.vercel.app/{art['image']}",
        "author": {
            "@type": "Organization",
            "name": "Premium AC Solutions Technical Editorial Team",
            "url": "https://acrepairnaplesfl-vercel.vercel.app/about"
        },
        "publisher": {
            "@type": "HVACBusiness",
            "@id": "https://acrepairnaplesfl-vercel.vercel.app/#localbusiness",
            "name": "Premium AC Solutions",
            "telephone": "+12396861066",
            "url": "https://acrepairnaplesfl-vercel.vercel.app/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "4389 Enterprise Avenue",
                "addressLocality": "Naples",
                "addressRegion": "FL",
                "postalCode": "34104",
                "addressCountry": "US"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}"
        }
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://acrepairnaplesfl-vercel.vercel.app/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://acrepairnaplesfl-vercel.vercel.app/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": art["title"],
                "item": f"https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}"
            }
        ]
    }

    schema_json_str = json.dumps(article_schema, indent=2)
    breadcrumb_json_str = json.dumps(breadcrumb_schema, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">

<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-684T43FDEM"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-684T43FDEM');
  </script>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="6yi7cacoszw7clEa9mq7gAq4vWRYRv0KIjPzy5me_Tg" />
  <title>{art['meta_title']}</title>
  <meta name="description" content="{art['meta_desc']}">
  <meta name="author" content="Premium AC Solutions">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}">

  <meta property="og:type" content="article">
  <meta property="og:title" content="{art['meta_title']}">
  <meta property="og:description" content="{art['meta_desc']}">
  <meta property="og:url" content="https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}">
  <meta property="og:image" content="https://acrepairnaplesfl-vercel.vercel.app/{art['image']}">
  <meta property="article:published_time" content="{art['date_iso']}">

  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/images/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="../assets/images/favicon-16x16.png" />
  <link rel="shortcut icon" href="../assets/images/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="../site.webmanifest" />
  <link rel="stylesheet" href="../assets/global.css" />

  <script type="application/ld+json">
{schema_json_str}
  </script>
  <script type="application/ld+json">
{breadcrumb_json_str}
  </script>
</head>

<body>
{get_header(depth=1)}

  <main id="main-content">
    <!-- Breadcrumbs -->
    <div class="site-container breadcrumbs" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span class="breadcrumb-separator">/</span>
      <a href="../blog.html">Blog</a>
      <span class="breadcrumb-separator">/</span>
      <span aria-current="page">{art['category']}</span>
    </div>

    <!-- Article Hero Banner -->
    <section class="page-hero" style="padding:3.5rem 0 2.5rem;">
      <div class="site-container" style="max-width:880px;">
        <div class="section-tag" style="background:rgba(2,132,199,0.15);color:#38bdf8;">{art['category']}</div>
        <h1 class="page-hero-title" style="font-size:clamp(1.9rem,3.5vw,2.8rem);margin-bottom:1rem;">
          {art['title']}
        </h1>

        <div style="display:flex;align-items:center;flex-wrap:wrap;gap:1.25rem;color:rgba(255,255,255,0.8);font-size:0.9rem;">
          <span style="display:flex;align-items:center;gap:0.45rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            {art['date']}
          </span>
          <span>&bull;</span>
          <span style="display:flex;align-items:center;gap:0.45rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {art['read_time']}
          </span>
          <span>&bull;</span>
          <span>By Premium AC Solutions Technical Team</span>
        </div>
      </div>
    </section>

    <!-- Main Article Body -->
    <article class="section" style="padding-top:2.5rem;">
      <div class="site-container" style="max-width:840px;">
        <!-- Featured Image Frame -->
        <div style="margin-bottom:2.5rem;border-radius:14px;overflow:hidden;box-shadow:var(--shadow-md);max-height:440px;">
          <img src="../{art['image']}" alt="{art['image_alt']}" style="width:100%;height:100%;object-fit:cover;display:block;" loading="eager" />
        </div>

        <div class="article-body" style="font-size:1.05rem;line-height:1.8;color:#334155;">
{art['content_html']}
        </div>

        <!-- Author Bio Box -->
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:1.75rem;margin-top:3rem;display:flex;gap:1.25rem;align-items:center;">
          <div style="width:52px;height:52px;border-radius:50%;background:#0f2438;color:#38bdf8;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1.1rem;">
            PA
          </div>
          <div>
            <h4 style="margin:0 0 0.25rem;font-size:1.05rem;color:#0f2438;">Premium AC Solutions Technical Team</h4>
            <p style="margin:0;font-size:0.88rem;line-height:1.55;color:#64748b;">
              Articles written and reviewed by licensed, EPA Universal Section 608 certified HVAC technicians with 15+ years of hands-on experience solving residential and commercial cooling problems across Naples and Collier County, FL.
            </p>
          </div>
        </div>

        <!-- Article Navigation -->
        <div style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
          <a href="../blog.html" style="color:#0284c7;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:0.4rem;">
            &larr; Back to All Guides
          </a>
          <a href="../contact.html" class="btn btn-primary" style="padding:0.65rem 1.25rem;font-size:0.9rem;">
            Schedule Technician Visit
          </a>
        </div>
      </div>
    </article>

    <!-- Related Articles Grid -->
    <section class="section section-alt" style="border-top:1px solid #e2e8f0;">
      <div class="site-container">
        <div class="section-header" style="margin-bottom:2rem;">
          <div class="section-tag">Related Guides</div>
          <h2 class="section-title">Recommended Cooling Reading</h2>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:1.75rem;">
{related_joined}
        </div>
      </div>
    </section>

    <!-- Bottom Lead Callout -->
    <section class="cta-banner">
      <div class="site-container">
        <div class="cta-banner-inner">
          <div style="max-width:680px;">
            <h2 class="cta-banner-title">Need Fast AC Service in Naples, FL?</h2>
            <p class="cta-banner-desc">We offer same-day diagnostics, upfront estimates, and 24/7 emergency response across Collier County.</p>
          </div>
          <div class="cta-banner-actions">
            <a href="tel:+12396861066" class="btn btn-primary" style="background:#fff;color:#0f2438;font-weight:700;">Call (239) 686-1066</a>
            <a href="../contact.html" class="btn btn-outline" style="border-color:#fff;color:#fff;">Contact Us Online</a>
          </div>
        </div>
      </div>
    </section>
  </main>

{get_footer(depth=1)}
</body>

</html>"""

def build_all():
    print("Building blog.html and blog/index.html...")
    blog_html = render_blog_listing_html(depth=0)
    with open("blog.html", "w", encoding="utf-8") as f:
        f.write(blog_html)
    print("blog.html written.")

    blog_folder_index = render_blog_listing_html(depth=1)
    os.makedirs("blog", exist_ok=True)
    with open("blog/index.html", "w", encoding="utf-8") as f:
        f.write(blog_folder_index)
    print("blog/index.html written.")

    print("Generating individual article pages in blog/...")
    for art in ALL_ARTICLES:
        filename = f"blog/{art['slug']}.html"
        content = render_article_page_html(art)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filename}")

    # Update _redirects
    print("Updating _redirects...")
    with open("_redirects", "r", encoding="utf-8") as f:
        redirects = f.read()

    new_redirects_lines = []
    for art in ALL_ARTICLES:
        slug = art['slug']
        line = f"/blog/{slug}.html /blog/{slug} 301!"
        if line not in redirects:
            new_redirects_lines.append(line)

    if new_redirects_lines:
        redirects = redirects.rstrip() + "\n" + "\n".join(new_redirects_lines) + "\n"
        with open("_redirects", "w", encoding="utf-8") as f:
            f.write(redirects)
        print("Updated _redirects with clean article routes.")

    # Update vercel.json
    print("Updating vercel.json...")
    with open("vercel.json", "r", encoding="utf-8") as f:
        vercel_cfg = json.load(f)

    existing_sources = {r["source"] for r in vercel_cfg.get("redirects", [])}
    for art in ALL_ARTICLES:
        slug = art['slug']
        src = f"/blog/{slug}.html"
        if src not in existing_sources:
            vercel_cfg["redirects"].append({
                "source": src,
                "destination": f"/blog/{slug}",
                "permanent": True
            })

    with open("vercel.json", "w", encoding="utf-8") as f:
        json.dump(vercel_cfg, f, indent=2)
    print("Updated vercel.json with clean article redirects.")

    # Update sitemap.xml
    print("Updating sitemap.xml...")
    with open("sitemap.xml", "r", encoding="utf-8") as f:
        sitemap = f.read()

    sitemap_entries = []
    if "https://acrepairnaplesfl-vercel.vercel.app/blog" not in sitemap:
        sitemap_entries.append("""    <url>
        <loc>https://acrepairnaplesfl-vercel.vercel.app/blog</loc>
        <lastmod>2026-10-13</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>""")

    for art in ALL_ARTICLES:
        slug = art['slug']
        url = f"https://acrepairnaplesfl-vercel.vercel.app/blog/{slug}"
        if url not in sitemap:
            sitemap_entries.append(f"""    <url>
        <loc>{url}</loc>
        <lastmod>2026-10-13</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")

    if sitemap_entries:
        sitemap = sitemap.replace("</urlset>", "\n".join(sitemap_entries) + "\n</urlset>")
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)
        print("Updated sitemap.xml with blog and 10 articles.")

    print("ALL BLOG GENERATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    build_all()
