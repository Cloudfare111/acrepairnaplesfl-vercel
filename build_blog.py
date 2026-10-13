# -*- coding: utf-8 -*-
"""
Main Builder Script for AC Repair Naples Fl Blog System
1. Combines articles from blog_data_1, blog_data_2, blog_data_3
2. Generates root blog.html
3. Generates blog/index.html
4. Generates 10 individual article HTML pages in blog/
5. Updates navigation in all 20 existing HTML files
6. Updates _redirects, vercel.json, and sitemap.xml
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

# Common Header & Footer snippets
def get_desktop_nav(depth=0):
    p = "../" if depth == 1 else ""
    return f"""      <nav aria-label="Primary" class="t6-nav-desktop">
        <a href="{p}index.html" class="t6-nav-link">Home</a>
        <a href="{p}about.html" class="t6-nav-link">About</a>
        <div class="t6-nav-dropdown">
          <a href="{p}services.html" class="t6-nav-link" aria-haspopup="true">Services <svg class="t6-nav-chevron"
              width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 9l6 6 6-6" />
            </svg></a>
          <div class="t6-nav-panel" role="menu">
            <div class="t6-nav-panel-grid">
              <a href="{p}mini-split-repair.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Mini-Split Repair</span>
                  <span class="t6-nav-panel-desc">Ductless system diagnosis, cleaning, and refrigerant leak repair.</span>
                </span>
              </a>
              <a href="{p}ac-not-cooling.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">AC Not Cooling</span>
                  <span class="t6-nav-panel-desc">Fast diagnosis for frozen coils, warm vents, and airflow restrictions.</span>
                </span>
              </a>
              <a href="{p}condensate-drain-clog.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Condensate Drain Clog</span>
                  <span class="t6-nav-panel-desc">Nitrogen line blowouts and float switch protection against leaks.</span>
                </span>
              </a>
              <a href="{p}hvac-system-replacement.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">HVAC System Replacement</span>
                  <span class="t6-nav-panel-desc">High-efficiency, variable-speed heat pump replacements in Naples.</span>
                </span>
              </a>
              <a href="{p}window-ac-installation.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Window AC Installation</span>
                  <span class="t6-nav-panel-desc">Secure, energy-efficient window cooling installation.</span>
                </span>
              </a>
              <a href="{p}compressor-valve-replacement.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Compressor Valve Replacement</span>
                  <span class="t6-nav-panel-desc">Restore cooling compression and fix internal valve failure.</span>
                </span>
              </a>
              <a href="{p}package-unit-repair.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Package Unit Repair</span>
                  <span class="t6-nav-panel-desc">Rooftop and ground packaged HVAC diagnostic and service.</span>
                </span>
              </a>
              <a href="{p}ac-maintenance-tune-up.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">AC Maintenance & Tune-Up</span>
                  <span class="t6-nav-panel-desc">Seasonal 24-point precision tune-ups maximizing efficiency.</span>
                </span>
              </a>
              <a href="{p}refrigerant-freon-recharge.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path
                      d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Refrigerant & Freon Recharge</span>
                  <span class="t6-nav-panel-desc">EPA-certified leak detection and precision R-410A recharging.</span>
                </span>
              </a>
            </div>
            <a href="{p}services.html" class="t6-nav-panel-all">View all services &rarr;</a>
          </div>
        </div>
        <div class="t6-nav-dropdown">
          <a href="{p}locations.html" class="t6-nav-link" aria-haspopup="true">Locations <svg class="t6-nav-chevron"
              width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 9l6 6 6-6" />
            </svg></a>
          <div class="t6-nav-panel" role="menu">
            <div class="t6-nav-panel-grid">
              <a href="{p}hvac-bayshore-arts-district.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Bayshore Arts District</span>
                  <span class="t6-nav-panel-desc">Local service in Bayshore Arts District</span>
                </span>
              </a>
              <a href="{p}hvac-aqualane-shores.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Aqualane Shores</span>
                  <span class="t6-nav-panel-desc">Local service in Aqualane Shores</span>
                </span>
              </a>
              <a href="{p}hvac-royal-harbor.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Royal Harbor</span>
                  <span class="t6-nav-panel-desc">Local service in Royal Harbor</span>
                </span>
              </a>
              <a href="{p}hvac-port-royal.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Port Royal</span>
                  <span class="t6-nav-panel-desc">Local service in Port Royal</span>
                </span>
              </a>
              <a href="{p}hvac-park-shore.html" class="t6-nav-panel-item">
                <span class="t6-nav-panel-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg></span>
                <span class="t6-nav-panel-text">
                  <span class="t6-nav-panel-title">Park Shore</span>
                  <span class="t6-nav-panel-desc">Local service in Park Shore</span>
                </span>
              </a>
            </div>
            <a href="{p}locations.html" class="t6-nav-panel-all">View all service areas &rarr;</a>
          </div>
        </div>
        <a href="{p}blog.html" class="t6-nav-link" style="color:var(--t6-green);font-weight:600;">Blog</a>
        <a href="{p}contact.html" class="t6-nav-link">Contact</a>
      </nav>"""

def get_mobile_drawer(depth=0):
    p = "../" if depth == 1 else ""
    return f"""    <div id="t6Drawer" class="t6-drawer" style="background:var(--t6-ink);border-top:1px solid rgba(255,255,255,.1);">
      <div class="t6-container" style="padding:1.25rem 1.5rem 1.75rem;">
        <ul
          style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.6rem;font-family:var(--font-body);font-weight:500;font-size:1rem;">
          <li><a href="{p}index.html"
              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Home</a>
          </li>
          <li><a href="{p}about.html"
              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">About</a>
          </li>
          <li><a href="{p}services.html"
              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Services</a>
          </li>
          <li><a href="{p}locations.html"
              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Locations</a>
          </li>
          <li><a href="{p}blog.html"
              style="color:var(--t6-green);text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);font-weight:600;">Blog</a>
          </li>
          <li><a href="{p}contact.html"
              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Contact</a>
          </li>
        </ul>
        <details style="margin-top:1.25rem;color:#fff;">
          <summary style="font-family:var(--font-display);cursor:pointer;font-weight:600;">Browse Services</summary>
          <ul
            style="list-style:none;padding:.6rem 0 0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.4rem .8rem;color:rgba(255,255,255,.85);">
            <li><a href="{p}mini-split-repair.html" class="t6-link-grow t6-link-grow--on-ink">Mini-Split Repair</a></li>
            <li><a href="{p}ac-not-cooling.html" class="t6-link-grow t6-link-grow--on-ink">AC Not Cooling</a></li>
            <li><a href="{p}condensate-drain-clog.html" class="t6-link-grow t6-link-grow--on-ink">Condensate Drain Clog</a></li>
            <li><a href="{p}hvac-system-replacement.html" class="t6-link-grow t6-link-grow--on-ink">HVAC System Replacement</a></li>
            <li><a href="{p}window-ac-installation.html" class="t6-link-grow t6-link-grow--on-ink">Window AC Installation</a></li>
            <li><a href="{p}compressor-valve-replacement.html" class="t6-link-grow t6-link-grow--on-ink">Compressor Valve Replacement</a></li>
            <li><a href="{p}package-unit-repair.html" class="t6-link-grow t6-link-grow--on-ink">Package Unit Repair</a></li>
            <li><a href="{p}ac-maintenance-tune-up.html" class="t6-link-grow t6-link-grow--on-ink">AC Maintenance & Tune-Up</a></li>
            <li><a href="{p}refrigerant-freon-recharge.html" class="t6-link-grow t6-link-grow--on-ink">Refrigerant & Freon Recharge</a></li>
          </ul>
        </details>
        <details style="margin-top:1rem;color:#fff;">
          <summary style="font-family:var(--font-display);cursor:pointer;font-weight:600;">Service Areas</summary>
          <ul
            style="list-style:none;padding:.6rem 0 0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.4rem .8rem;color:rgba(255,255,255,.85);">
            <li><a href="{p}hvac-bayshore-arts-district.html" class="t6-link-grow t6-link-grow--on-ink">Bayshore Arts District</a></li>
            <li><a href="{p}hvac-aqualane-shores.html" class="t6-link-grow t6-link-grow--on-ink">Aqualane Shores</a></li>
            <li><a href="{p}hvac-royal-harbor.html" class="t6-link-grow t6-link-grow--on-ink">Royal Harbor</a></li>
            <li><a href="{p}hvac-port-royal.html" class="t6-link-grow t6-link-grow--on-ink">Port Royal</a></li>
            <li><a href="{p}hvac-park-shore.html" class="t6-link-grow t6-link-grow--on-ink">Park Shore</a></li>
          </ul>
        </details>
        <a href="tel:+12396861066" class="t6-btn t6-btn-primary" style="margin-top:1.5rem;width:100%;">Call (239) 686-1066</a>
      </div>
    </div>"""

def get_footer(depth=0):
    p = "../" if depth == 1 else ""
    return f"""  <footer class="t6-band-ink" style="padding:4.5rem 0 2.5rem;border-top:1px solid rgba(255,255,255,.1);">
    <div class="t6-container">
      <div style="display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2.5rem;margin-bottom:3rem;">
        <div>
          <a href="{p}index.html"
            style="display:inline-block;text-decoration:none;margin-bottom:1.25rem;" aria-label="Premium AC Solutions">
            <img src="{p}assets/images/logo-white.png" alt="Premium AC Solutions Logo" width="214" height="50"
              style="height:50px;width:auto;max-width:220px;object-fit:contain;display:block;" />
          </a>
          <p style="color:rgba(255,255,255,.75);font-size:.92rem;line-height:1.65;max-width:320px;margin-bottom:1.5rem;">
            Providing reliable AC repair, maintenance, and emergency HVAC solutions across Naples, FL and surrounding Collier County communities.
          </p>
          <div style="display:flex;gap:.65rem;align-items:center;">
            <a href="#" data-social="facebook" aria-label="Facebook"
              style="color:#fff;display:inline-flex;width:36px;height:36px;border:1px solid rgba(255,255,255,.25);border-radius:50%;align-items:center;justify-content:center;text-decoration:none;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
            </a>
            <a href="#" data-social="twitter" aria-label="X (Twitter)"
              style="color:#fff;display:inline-flex;width:36px;height:36px;border:1px solid rgba(255,255,255,.25);border-radius:50%;align-items:center;justify-content:center;text-decoration:none;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M10.488 14.651L15.25 21h7l-7.858-10.478L20.93 3h-2.65l-5.117 5.886L8.75 3h-7l7.51 10.015L2.32 21h2.65zM16.25 19L5.75 5h2l10.5 14z" />
              </svg>
            </a>
            <a href="#" data-social="youtube" aria-label="YouTube"
              style="color:#fff;display:inline-flex;width:36px;height:36px;border:1px solid rgba(255,255,255,.25);border-radius:50%;align-items:center;justify-content:center;text-decoration:none;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
              </svg>
            </a>
          </div>
        </div>

        <div>
          <p style="color:#fff;font-family:var(--font-display);font-weight:600;font-size:1rem;margin:0 0 1rem;">Contact</p>
          <hr class="t6-hr-green" style="margin:0 0 1rem;" />
          <div style="color:rgba(255,255,255,.85);font-size:.92rem;line-height:1.7;">
            <p style="margin:0 0 .4rem;"><a href="tel:+12396861066"
                style="color:#fff;text-decoration:none;font-weight:600;">(239) 686-1066</a></p>
            <p style="margin:0 0 .4rem;"><a href="https://maps.google.com/?q=4389+Enterprise+Avenue,+Naples,+FL+34104" target="_blank" rel="noopener noreferrer" style="color:rgba(255,255,255,.85);text-decoration:none;" title="View Premium AC Solutions on Google Maps">4389 Enterprise Avenue, Naples, FL 34104</a></p>
            <p style="margin:0;">Mon&ndash;Fri: 7AM &ndash; 7PM<br />Sat: 8AM &ndash; 4PM<br />24/7 Emergency</p>
          </div>
        </div>

        <div>
          <p style="color:#fff;font-family:var(--font-display);font-weight:600;font-size:1rem;margin:0 0 1rem;">Services</p>
          <hr class="t6-hr-green" style="margin:0 0 1rem;" />
          <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.5rem;font-size:.92rem;">
            <li><a href="{p}mini-split-repair.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Mini-Split Repair</a></li>
            <li><a href="{p}ac-not-cooling.html" style="color:rgba(255,255,255,.85);text-decoration:none;">AC Not Cooling</a></li>
            <li><a href="{p}condensate-drain-clog.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Condensate Drain Clog</a></li>
            <li><a href="{p}hvac-system-replacement.html" style="color:rgba(255,255,255,.85);text-decoration:none;">HVAC System Replacement</a></li>
            <li><a href="{p}ac-maintenance-tune-up.html" style="color:rgba(255,255,255,.85);text-decoration:none;">AC Maintenance & Tune-Up</a></li>
            <li><a href="{p}refrigerant-freon-recharge.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Refrigerant & Freon Recharge</a></li>
            <li><a href="{p}services.html" class="t6-link-grow t6-link-grow--on-ink" style="color:var(--t6-green);">View All &rarr;</a></li>
          </ul>
        </div>

        <div>
          <p style="color:#fff;font-family:var(--font-display);font-weight:600;font-size:1rem;margin:0 0 1rem;">Quick Links</p>
          <hr class="t6-hr-green" style="margin:0 0 1rem;" />
          <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.5rem;font-size:.92rem;">
            <li><a href="{p}about.html" style="color:rgba(255,255,255,.85);text-decoration:none;">About Us</a></li>
            <li><a href="{p}locations.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Service Areas</a></li>
            <li><a href="{p}blog.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Blog & Knowledge Hub</a></li>
            <li><a href="{p}contact.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Contact</a></li>
            <li><a href="{p}privacy-policy.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Privacy Policy</a></li>
          </ul>
        </div>
      </div>

      <div
        style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,.12);display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;align-items:center;color:rgba(255,255,255,.6);font-size:.85rem;">
        <p style="margin:0;">&copy; 2026 Premium AC Solutions. Licensed &amp; insured. All rights reserved.</p>
        <p style="margin:0;display:flex;gap:1rem;align-items:center;">
          <span style="display:inline-flex;gap:6px;align-items:center;">
            <span style="font-family:var(--font-display);font-weight:700;color:var(--t6-green);">VISA</span>
            <span style="font-family:var(--font-display);font-weight:700;color:var(--t6-green);">MC</span>
            <span style="font-family:var(--font-display);font-weight:700;color:var(--t6-green);">AMEX</span>
            <span style="font-family:var(--font-display);font-weight:700;color:var(--t6-green);">CASH</span>
          </span>
        </p>
      </div>
    </div>
  </footer>

  <div class="t6-mobile-cta" role="region" aria-label="Mobile call to action">
    <a href="tel:+12396861066" class="t6-mobile-cta__call">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round">
        <path
          d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" />
      </svg>
      Call (239) 686-1066
    </a>
    <a href="{p}contact.html" class="t6-mobile-cta__quote">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
      Get Quote
    </a>
  </div>
  <div class="t6-rail" role="region" aria-label="Quick contact rail">
    <a href="tel:+12396861066">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round">
        <path
          d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" />
      </svg>
      Call
    </a>
    <a href="{p}contact.html">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
      Quote
    </a>
  </div>
  <script src="https://unpkg.com/sal.js"></script>
  <script src="{p}assets/js/main.js"></script>"""

def render_trust_strip():
    return """<section class="t6-trust-strip" aria-label="Why customers trust us">
  <div class="t6-container">
    <div class="t6-trust-strip__grid">
      <div class="t6-trust-item" data-sal="fade">
        <span class="t6-trust-item__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg></span>
        <span style="display:flex;flex-direction:column;gap:2px;">
          <span class="t6-trust-item__label">Licensed</span>
          <span class="t6-trust-item__value">Licensed & Bonded</span>
        </span>
      </div>
      <div class="t6-trust-item" data-sal="fade">
        <span class="t6-trust-item__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></span>
        <span style="display:flex;flex-direction:column;gap:2px;">
          <span class="t6-trust-item__label">Fully Insured</span>
          <span class="t6-trust-item__value">Insured & Bonded</span>
        </span>
      </div>
      <div class="t6-trust-item" data-sal="fade">
        <span class="t6-trust-item__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></span>
        <span style="display:flex;flex-direction:column;gap:2px;">
          <span class="t6-trust-item__label">24/7 Emergency</span>
          <span class="t6-trust-item__value">Same-Day Response</span>
        </span>
      </div>
      <div class="t6-trust-item" data-sal="fade">
        <span class="t6-trust-item__icon"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg></span>
        <span style="display:flex;flex-direction:column;gap:2px;">
          <span class="t6-trust-item__label">Warranty Backed</span>
          <span class="t6-trust-item__value">Guaranteed in Naples</span>
        </span>
      </div>
    </div>
  </div>
</section>"""

def render_blog_listing_html(depth=0):
    p = "../" if depth == 1 else ""
    card_link_prefix = "" if depth == 1 else "blog/"
    
    cards_html = []
    for art in ALL_ARTICLES:
        card = f"""      <article class="t6-blog-card" data-sal="slide-up">
        <div class="t6-blog-card__image-wrap">
          <a href="{card_link_prefix}{art['slug']}.html" tabindex="-1" aria-hidden="true">
            <img src="{p}{art['image']}" alt="{art['image_alt']}" class="t6-blog-card__image" loading="lazy" />
          </a>
          <span style="position:absolute;top:14px;left:14px;z-index:2;">
            <span class="t6-blog-category">{art['category']}</span>
          </span>
        </div>
        <div class="t6-blog-card__body">
          <div class="t6-blog-meta">
            <span>{art['date']}</span>
            <span>&bull;</span>
            <span class="t6-blog-read-time">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              {art['read_time']}
            </span>
          </div>
          <h2 class="t6-blog-card__title">
            <a href="{card_link_prefix}{art['slug']}.html">{art['title']}</a>
          </h2>
          <p class="t6-blog-card__excerpt">{art['excerpt']}</p>
          <div class="t6-blog-card__footer">
            <a href="{card_link_prefix}{art['slug']}.html" class="t6-link-grow">
              Read Article <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
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
        "@id": "https://acrepairnaplesfl.com/blog#blog",
        "name": "Premium AC Solutions Knowledge Hub & Blog",
        "description": "Expert air conditioning repair guides, troubleshooting advice, and seasonal cooling tips from licensed technicians in Naples, Florida.",
        "url": "https://acrepairnaplesfl.com/blog",
        "publisher": {
            "@type": "LocalBusiness",
            "@id": "https://acrepairnaplesfl.com/#localbusiness",
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
                "url": f"https://acrepairnaplesfl.com/blog/{a['slug']}",
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
  <title>HVAC & AC Repair Blog Naples FL | Expert Homeowner Guides</title>
  <meta name="description"
    content="Practical air conditioning troubleshooting guides, energy-saving tips, and HVAC maintenance advice from licensed cooling technicians in Naples, Florida.">
  <meta name="author" content="Premium AC Solutions">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://acrepairnaplesfl.com/blog">

  <meta property="og:type" content="website">
  <meta property="og:title" content="HVAC & AC Repair Blog Naples FL | Expert Homeowner Guides">
  <meta property="og:description"
    content="Practical air conditioning troubleshooting guides, energy-saving tips, and HVAC maintenance advice from licensed cooling technicians in Naples, Florida.">
  <meta property="og:url" content="https://acrepairnaplesfl.com/blog">
  <meta property="og:image" content="{p}assets/images/services/ac-not-cooling.webp">

  <link rel="icon" type="image/svg+xml" href="{p}assets/images/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="{p}assets/images/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="{p}assets/images/favicon-16x16.png" />
  <link rel="shortcut icon" href="{p}assets/images/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="{p}assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="{p}site.webmanifest" />
  <link rel="stylesheet" href="{p}assets/global.css" />
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

  <script type="application/ld+json">
{schema_json_str}
  </script>
</head>

<body>

  <header
    style="position:sticky;top:0;z-index:50;background:#fff;color:var(--t6-ink);border-bottom:1px solid var(--t6-hairline);box-shadow:0 1px 0 rgba(23,34,7,0.04);">
    <div class="t6-container"
      style="display:flex;align-items:center;justify-content:space-between;gap:1.5rem;padding-top:0.95rem;padding-bottom:0.95rem;">
      <a href="{p}index.html" style="display:flex;align-items:center;text-decoration:none;" aria-label="Premium AC Solutions">
        <img src="{p}assets/images/logo.png" alt="Premium AC Solutions Logo" width="214" height="50"
          style="height:50px;width:auto;max-width:220px;object-fit:contain;display:block;" />
      </a>

{get_desktop_nav(depth)}

      <div style="display:flex;align-items:center;gap:.85rem;">
        <a class="t6-btn t6-btn-primary" href="tel:+12396861066">Get Estimate</a>
        <button id="t6NavToggle" aria-label="Open menu" aria-expanded="false" aria-controls="t6Drawer"
          class="t6-nav-toggle"
          style="background:transparent;border:1px solid var(--t6-hairline);color:var(--t6-ink);width:42px;height:42px;border-radius:8px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>

{get_mobile_drawer(depth)}

    <style>
      .t6-nav-desktop {{ display: none; align-items: center; gap: 1.85rem; font-family: var(--font-body); font-weight: 500; font-size: 0.95rem; }}
      .t6-nav-link {{ display: inline-flex; align-items: center; gap: 0.3rem; color: var(--t6-ink); text-decoration: none; padding: 0.4rem 0; }}
      .t6-nav-link:hover {{ color: var(--t6-green-dark); }}
      .t6-nav-chevron {{ transition: transform 0.2s ease; }}
      .t6-nav-dropdown {{ position: relative; }}
      .t6-nav-dropdown > .t6-nav-link {{ cursor: pointer; }}
      .t6-nav-panel {{ position: absolute; top: 100%; left: 50%; transform: translateX(-50%) translateY(8px); width: 540px; background: #fff; border: 1px solid var(--t6-hairline); border-radius: 12px; box-shadow: 0 18px 50px rgba(23, 34, 7, 0.13); padding: 1.25rem; opacity: 0; visibility: hidden; transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease; z-index: 50; }}
      .t6-nav-dropdown:hover > .t6-nav-panel, .t6-nav-dropdown:focus-within > .t6-nav-panel {{ opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }}
      .t6-nav-dropdown:hover .t6-nav-chevron, .t6-nav-dropdown:focus-within .t6-nav-chevron {{ transform: rotate(180deg); }}
      .t6-nav-panel-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.45rem; max-height: 380px; overflow-y: auto; }}
      .t6-nav-panel-item {{ display: flex; gap: 0.7rem; align-items: flex-start; padding: 0.7rem 0.8rem; border-radius: 8px; text-decoration: none; color: var(--t6-ink); transition: background 0.15s ease; }}
      .t6-nav-panel-item:hover {{ background: var(--t6-band); color: var(--t6-ink); }}
      .t6-nav-panel-icon {{ flex: 0 0 36px; width: 36px; height: 36px; background: rgba(169, 223, 89, 0.22); border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: var(--t6-ink); }}
      .t6-nav-panel-text {{ flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 0.2rem; }}
      .t6-nav-panel-title {{ font-family: var(--font-display); font-weight: 600; font-size: 0.92rem; line-height: 1.2; color: var(--t6-ink); }}
      .t6-nav-panel-desc {{ font-size: 0.78rem; color: var(--t6-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
      .t6-nav-panel-all {{ display: block; margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid var(--t6-hairline); font-family: var(--font-display); font-weight: 600; font-size: 0.88rem; color: var(--t6-ink); text-decoration: none; }}
      .t6-nav-panel-all:hover {{ color: var(--t6-green-dark); }}
      @media (min-width: 1024px) {{ .t6-nav-desktop {{ display: flex !important; }} .t6-nav-toggle {{ display: none !important; }} }}
    </style>
  </header>

  <main>
    <!-- Hero Section -->
    <section class="t6-band-ink" style="position:relative;padding:6.5rem 0 4.5rem;overflow:hidden;">
      <div style="position:absolute;inset:0;background:url('{p}assets/images/gen/on-the-job-a6ed251e.webp') center/cover no-repeat;opacity:.28;"></div>
      <div class="t6-hero-overlay"></div>
      <div class="t6-container" style="position:relative;text-align:center;">
        <ul style="display:inline-flex;gap:.75rem;margin:0 0 1.25rem;padding:0;list-style:none;font-family:var(--font-body);font-weight:500;text-transform:uppercase;letter-spacing:.14em;font-size:.78rem;" data-sal="fade">
          <li style="color:rgba(255,255,255,.78);"><a href="{p}index.html" style="color:inherit;text-decoration:none;">Home</a></li>
          <li style="display:flex;align-items:center;gap:.5rem;color:var(--t6-green);"><span style="opacity:.5;">/</span>AC &amp; HVAC Blog</li>
        </ul>
        <h1 style="color:#fff;margin:0 auto 1.2rem;max-width:880px;" data-sal="slide-up">Naples AC Repair &amp; HVAC Knowledge Hub</h1>
        <hr class="t6-hr-green" style="margin:1rem auto 1.25rem;" />
        <p style="color:rgba(255,255,255,.88);max-width:720px;margin:0 auto;font-size:1.1rem;line-height:1.7;" data-sal="fade" data-sal-delay="100">
          Expert cooling advice, troubleshooting guides, and seasonal maintenance wisdom written by licensed, EPA-certified HVAC professionals serving homeowners across Naples, FL.
        </p>
      </div>
    </section>

{render_trust_strip()}

    <!-- Category Filter Strip -->
    <section class="t6-section--tight t6-band-white" style="border-bottom:1px solid var(--t6-hairline);">
      <div class="t6-container">
        <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:.65rem;">
          <span class="t6-pill t6-pill--green" style="color:#fff;">All 10 Guides</span>
          <span class="t6-pill">Troubleshooting</span>
          <span class="t6-pill">Cooling Performance</span>
          <span class="t6-pill">Leaks &amp; Drains</span>
          <span class="t6-pill">Refrigerant &amp; Coils</span>
          <span class="t6-pill">Maintenance &amp; Safety</span>
        </div>
      </div>
    </section>

    <!-- Blog Grid Section -->
    <section class="t6-section t6-band-cream">
      <div class="t6-container">
        <div class="t6-section-title t6-section-title--center" data-sal="fade">
          <span class="t6-eyebrow">Practical Homeowner Insights</span>
          <h2 style="margin:.4rem 0 .75rem;">Latest HVAC Guides &amp; Expert Solutions</h2>
          <p class="t6-section-title__lede">
            Browse our original articles answering the most pressing cooling, drainage, and mechanical questions for Southwest Florida residences.
          </p>
        </div>

        <div class="t6-blog-grid">
{cards_joined}
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="t6-band-ink" style="padding:4.5rem 0;position:relative;">
      <div class="t6-container" style="text-align:center;">
        <span class="t6-eyebrow t6-eyebrow--on-ink">Need Rapid Help in Collier County?</span>
        <h2 style="color:#fff;margin:.5rem 0 1rem;font-size:clamp(1.75rem,3.5vw,2.5rem);">Don't Let AC Trouble Ruin Your Florida Comfort</h2>
        <p style="color:rgba(255,255,255,.82);max-width:640px;margin:0 auto 2rem;font-size:1.05rem;line-height:1.7;">
          From frozen coils and clogged condensate lines to emergency compressor repairs, our certified Naples technicians arrive with same-day diagnostic service and upfront pricing.
        </p>
        <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
          <a href="tel:+12396861066" class="t6-btn t6-btn-primary">Call (239) 686-1066</a>
          <a href="{p}contact.html" class="t6-btn t6-btn-ghost-on-ink">Request Service Online</a>
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
        card = f"""        <article class="t6-blog-card">
          <div class="t6-blog-card__image-wrap">
            <a href="{r['slug']}.html" tabindex="-1">
              <img src="../{r['image']}" alt="{r['image_alt']}" class="t6-blog-card__image" loading="lazy" />
            </a>
            <span style="position:absolute;top:12px;left:12px;z-index:2;">
              <span class="t6-blog-category">{r['category']}</span>
            </span>
          </div>
          <div class="t6-blog-card__body">
            <div class="t6-blog-meta">
              <span>{r['date']}</span>
              <span>&bull;</span>
              <span>{r['read_time']}</span>
            </div>
            <h3 class="t6-blog-card__title" style="font-size:1.15rem;">
              <a href="{r['slug']}.html">{r['title']}</a>
            </h3>
            <p class="t6-blog-card__excerpt" style="font-size:.9rem;line-height:1.5;">{r['excerpt']}</p>
            <div class="t6-blog-card__footer">
              <a href="{r['slug']}.html" class="t6-link-grow" style="font-size:.9rem;">
                Read Article &rarr;
              </a>
            </div>
          </div>
        </article>"""
        related_cards.append(card)
    related_joined = "\n".join(related_cards)

    # Article Schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": f"https://acrepairnaplesfl.com/blog/{slug}#article",
        "headline": art["title"],
        "description": art["meta_desc"],
        "url": f"https://acrepairnaplesfl.com/blog/{slug}",
        "datePublished": art["date_iso"],
        "dateModified": art["date_iso"],
        "image": f"https://acrepairnaplesfl.com/{art['image']}",
        "author": {
            "@type": "Organization",
            "name": "Premium AC Solutions Technical Editorial Team",
            "url": "https://acrepairnaplesfl.com/about"
        },
        "publisher": {
            "@type": "LocalBusiness",
            "@id": "https://acrepairnaplesfl.com/#localbusiness",
            "name": "Premium AC Solutions",
            "telephone": "+12396861066",
            "url": "https://acrepairnaplesfl.com/",
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
            "@id": f"https://acrepairnaplesfl.com/blog/{slug}"
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
                "item": "https://acrepairnaplesfl.com/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://acrepairnaplesfl.com/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": art["title"],
                "item": f"https://acrepairnaplesfl.com/blog/{slug}"
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
  <link rel="canonical" href="https://acrepairnaplesfl.com/blog/{slug}">

  <meta property="og:type" content="article">
  <meta property="og:title" content="{art['meta_title']}">
  <meta property="og:description" content="{art['meta_desc']}">
  <meta property="og:url" content="https://acrepairnaplesfl.com/blog/{slug}">
  <meta property="og:image" content="https://acrepairnaplesfl.com/{art['image']}">
  <meta property="article:published_time" content="{art['date_iso']}">

  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="../assets/images/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="../assets/images/favicon-16x16.png" />
  <link rel="shortcut icon" href="../assets/images/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/images/apple-touch-icon.png" />
  <link rel="manifest" href="../site.webmanifest" />
  <link rel="stylesheet" href="../assets/global.css" />
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

  <script type="application/ld+json">
{schema_json_str}
  </script>
  <script type="application/ld+json">
{breadcrumb_json_str}
  </script>
</head>

<body>

  <header
    style="position:sticky;top:0;z-index:50;background:#fff;color:var(--t6-ink);border-bottom:1px solid var(--t6-hairline);box-shadow:0 1px 0 rgba(23,34,7,0.04);">
    <div class="t6-container"
      style="display:flex;align-items:center;justify-content:space-between;gap:1.5rem;padding-top:0.95rem;padding-bottom:0.95rem;">
      <a href="../index.html" style="display:flex;align-items:center;text-decoration:none;" aria-label="Premium AC Solutions">
        <img src="../assets/images/logo.png" alt="Premium AC Solutions Logo" width="214" height="50"
          style="height:50px;width:auto;max-width:220px;object-fit:contain;display:block;" />
      </a>

{get_desktop_nav(depth=1)}

      <div style="display:flex;align-items:center;gap:.85rem;">
        <a class="t6-btn t6-btn-primary" href="tel:+12396861066">Get Estimate</a>
        <button id="t6NavToggle" aria-label="Open menu" aria-expanded="false" aria-controls="t6Drawer"
          class="t6-nav-toggle"
          style="background:transparent;border:1px solid var(--t6-hairline);color:var(--t6-ink);width:42px;height:42px;border-radius:8px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>

{get_mobile_drawer(depth=1)}

    <style>
      .t6-nav-desktop {{ display: none; align-items: center; gap: 1.85rem; font-family: var(--font-body); font-weight: 500; font-size: 0.95rem; }}
      .t6-nav-link {{ display: inline-flex; align-items: center; gap: 0.3rem; color: var(--t6-ink); text-decoration: none; padding: 0.4rem 0; }}
      .t6-nav-link:hover {{ color: var(--t6-green-dark); }}
      .t6-nav-chevron {{ transition: transform 0.2s ease; }}
      .t6-nav-dropdown {{ position: relative; }}
      .t6-nav-dropdown > .t6-nav-link {{ cursor: pointer; }}
      .t6-nav-panel {{ position: absolute; top: 100%; left: 50%; transform: translateX(-50%) translateY(8px); width: 540px; background: #fff; border: 1px solid var(--t6-hairline); border-radius: 12px; box-shadow: 0 18px 50px rgba(23, 34, 7, 0.13); padding: 1.25rem; opacity: 0; visibility: hidden; transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease; z-index: 50; }}
      .t6-nav-dropdown:hover > .t6-nav-panel, .t6-nav-dropdown:focus-within > .t6-nav-panel {{ opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }}
      .t6-nav-dropdown:hover .t6-nav-chevron, .t6-nav-dropdown:focus-within .t6-nav-chevron {{ transform: rotate(180deg); }}
      .t6-nav-panel-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.45rem; max-height: 380px; overflow-y: auto; }}
      .t6-nav-panel-item {{ display: flex; gap: 0.7rem; align-items: flex-start; padding: 0.7rem 0.8rem; border-radius: 8px; text-decoration: none; color: var(--t6-ink); transition: background 0.15s ease; }}
      .t6-nav-panel-item:hover {{ background: var(--t6-band); color: var(--t6-ink); }}
      .t6-nav-panel-icon {{ flex: 0 0 36px; width: 36px; height: 36px; background: rgba(169, 223, 89, 0.22); border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: var(--t6-ink); }}
      .t6-nav-panel-text {{ flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 0.2rem; }}
      .t6-nav-panel-title {{ font-family: var(--font-display); font-weight: 600; font-size: 0.92rem; line-height: 1.2; color: var(--t6-ink); }}
      .t6-nav-panel-desc {{ font-size: 0.78rem; color: var(--t6-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
      .t6-nav-panel-all {{ display: block; margin-top: 1rem; padding-top: 0.85rem; border-top: 1px solid var(--t6-hairline); font-family: var(--font-display); font-weight: 600; font-size: 0.88rem; color: var(--t6-ink); text-decoration: none; }}
      .t6-nav-panel-all:hover {{ color: var(--t6-green-dark); }}
      @media (min-width: 1024px) {{ .t6-nav-desktop {{ display: flex !important; }} .t6-nav-toggle {{ display: none !important; }} }}
    </style>
  </header>

  <main>
    <!-- Article Hero Banner -->
    <section class="t6-band-ink" style="position:relative;padding:5.5rem 0 3.5rem;overflow:hidden;">
      <div style="position:absolute;inset:0;background:url('../assets/images/gen/on-the-job-a6ed251e.webp') center/cover no-repeat;opacity:.2;"></div>
      <div class="t6-hero-overlay"></div>
      <div class="t6-container" style="position:relative;max-width:880px;">
        <nav aria-label="Breadcrumb" style="margin-bottom:1.25rem;">
          <ol style="display:flex;flex-wrap:wrap;gap:.6rem;list-style:none;margin:0;padding:0;font-family:var(--font-display);text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:rgba(255,255,255,.7);">
            <li><a href="../index.html" style="color:inherit;text-decoration:none;">Home</a></li>
            <li>/</li>
            <li><a href="../blog.html" style="color:inherit;text-decoration:none;">Blog</a></li>
            <li>/</li>
            <li style="color:var(--t6-green);">{art['category']}</li>
          </ol>
        </nav>

        <span class="t6-blog-category" style="margin-bottom:1rem;">{art['category']}</span>
        <h1 style="color:#fff;margin:0 0 1.25rem;font-size:clamp(1.9rem,4vw,2.9rem);line-height:1.18;letter-spacing:-0.02em;">
          {art['title']}
        </h1>

        <div style="display:flex;align-items:center;flex-wrap:wrap;gap:1.25rem;color:rgba(255,255,255,.8);font-size:.9rem;">
          <span style="display:flex;align-items:center;gap:.45rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            {art['date']}
          </span>
          <span>&bull;</span>
          <span style="display:flex;align-items:center;gap:.45rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {art['read_time']}
          </span>
          <span>&bull;</span>
          <span>Written by Premium AC Solutions Technical Team</span>
        </div>
      </div>
    </section>

    <!-- Main Article Body -->
    <article class="t6-section t6-band-white">
      <div class="t6-article-container">
        <!-- Featured Image Frame -->
        <div class="t6-image-frame t6-image-frame--landscape" style="margin-bottom:2.75rem;border-radius:14px;">
          <img src="../{art['image']}" alt="{art['image_alt']}" style="width:100%;height:100%;object-fit:cover;" loading="eager" />
        </div>

        <div class="t6-article-content">
{art['content_html']}
        </div>

        <!-- Author Bio Box -->
        <div class="t6-article-author-card">
          <div class="t6-article-author-avatar">PA</div>
          <div>
            <h4 style="margin:0 0 .25rem;font-size:1.1rem;color:var(--t6-ink);">Premium AC Solutions Technical Editorial Team</h4>
            <p style="margin:0;font-size:.92rem;line-height:1.55;color:var(--t6-muted);">
              Our articles are written and verified by state-certified, EPA Section 608 universal technicians with over 20 years of hands-on experience solving residential and commercial air conditioning challenges throughout Naples and Southwest Florida.
            </p>
          </div>
        </div>

        <!-- Back to Blog Link -->
        <div style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--t6-hairline);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
          <a href="../blog.html" class="t6-link-grow" style="font-weight:700;">
            &larr; Back to All Blog Guides
          </a>
          <a href="../contact.html" class="t6-btn t6-btn-primary" style="padding:10px 20px;font-size:.9rem;">
            Schedule Technician Visit
          </a>
        </div>
      </div>
    </article>

    <!-- Related Articles Grid -->
    <section class="t6-section t6-band-cream" style="border-top:1px solid var(--t6-hairline);">
      <div class="t6-container">
        <div class="t6-section-title" style="margin-bottom:2rem;">
          <span class="t6-eyebrow">Related Reading</span>
          <h2 style="font-size:1.85rem;margin:0;">Recommended Cooling Guides</h2>
        </div>

        <div class="t6-blog-grid">
{related_joined}
        </div>
      </div>
    </section>

    <!-- Bottom Sticky Lead Callout -->
    <section class="t6-band-green" style="padding:3.5rem 0;">
      <div class="t6-container" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;">
        <div>
          <h3 style="color:#fff;margin:0 0 .35rem;font-size:1.5rem;">Need Fast AC Service in Naples, FL?</h3>
          <p style="color:rgba(255,255,255,.9);margin:0;font-size:1rem;">We offer same-day diagnostics, upfront estimates, and 24/7 emergency response.</p>
        </div>
        <div style="display:flex;gap:.85rem;flex-wrap:wrap;">
          <a href="tel:+12396861066" class="t6-btn t6-btn-on-green" style="background:#fff;color:var(--t6-ink);">Call (239) 686-1066</a>
          <a href="../contact.html" class="t6-btn t6-btn-ghost-on-ink" style="border-color:#fff;color:#fff;">Contact Us Online</a>
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

    # Navigation update across all 20 root HTML files
    print("Updating navigation across existing HTML files...")
    root_files = glob.glob("*.html")
    for fpath in root_files:
        if fpath in ["404.html", "blog.html"]:
            continue
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        modified = False

        # 1. Desktop Nav: insert Blog before Contact if not already present
        if 'href="blog.html"' not in content and 'href="/blog"' not in content:
            # Pattern in desktop nav: <a href="contact.html" class="t6-nav-link">Contact</a>
            desktop_target = '<a href="contact.html" class="t6-nav-link">Contact</a>'
            desktop_replacement = '<a href="blog.html" class="t6-nav-link">Blog</a>\n        <a href="contact.html" class="t6-nav-link">Contact</a>'
            if desktop_target in content:
                content = content.replace(desktop_target, desktop_replacement)
                modified = True

            # 2. Mobile Drawer: insert Blog before Contact
            drawer_pattern_1 = '<li><a href="contact.html"\n              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Contact</a>\n          </li>'
            drawer_replacement_1 = '<li><a href="blog.html"\n              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Blog</a>\n          </li>\n          <li><a href="contact.html"\n              style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Contact</a>\n          </li>'
            
            drawer_pattern_2 = '<li><a href="contact.html" style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Contact</a></li>'
            drawer_replacement_2 = '<li><a href="blog.html" style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Blog</a></li>\n        <li><a href="contact.html" style="color:#fff;text-decoration:none;display:block;padding:.55rem 0;border-bottom:1px solid rgba(255,255,255,.08);">Contact</a></li>'

            if drawer_pattern_1 in content:
                content = content.replace(drawer_pattern_1, drawer_replacement_1)
                modified = True
            elif drawer_pattern_2 in content:
                content = content.replace(drawer_pattern_2, drawer_replacement_2)
                modified = True

            # 3. Footer Quick Links: insert Blog before Contact
            footer_pattern = '<li><a href="contact.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Contact</a></li>'
            footer_replacement = '<li><a href="blog.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Blog</a></li>\n            <li><a href="contact.html" style="color:rgba(255,255,255,.85);text-decoration:none;">Contact</a></li>'
            if footer_pattern in content:
                content = content.replace(footer_pattern, footer_replacement)
                modified = True

        if modified:
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(content)
            print(f"Updated navigation in {fpath}")

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
    if "https://acrepairnaplesfl.com/blog" not in sitemap:
        sitemap_entries.append("""    <url>
        <loc>https://acrepairnaplesfl.com/blog</loc>
        <lastmod>2026-10-07</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>""")

    for art in ALL_ARTICLES:
        slug = art['slug']
        url = f"https://acrepairnaplesfl.com/blog/{slug}"
        if url not in sitemap:
            sitemap_entries.append(f"""    <url>
        <loc>{url}</loc>
        <lastmod>2026-10-07</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")

    if sitemap_entries:
        sitemap = sitemap.replace("</urlset>", "\n".join(sitemap_entries) + "\n</urlset>")
        with open("sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap)
        print("Updated sitemap.xml with blog and 10 articles.")

    print("ALL BLOG GENERATION & SITE INTEGRATION COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    build_all()
