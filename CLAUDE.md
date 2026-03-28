# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a collection of personal utility scripts and tools, primarily focused on:
- Data cleaning of employee CSV files
- DNS troubleshooting for GitHub access
- Custom Claude Code skills
- Chinese content creation (WeChat public account articles)

The codebase is not a traditional software project with build systems or tests, but rather a toolkit for specific tasks.

## Data Cleaning Scripts

Three Python scripts for cleaning employee data CSV files:

1. `clean_employee_data.py` - Uses pandas for comprehensive data cleaning
   - Loads `dirty_employee_data.csv`
   - Cleans all columns: employee ID, name, age, salary, join date, email, department, status, performance rating, remarks
   - Outputs `cleaned_employee_data.csv`

2. `clean_employee_data_csv.py` - Uses Python's csv module (no pandas dependency)
   - Similar functionality but uses standard library only
   - Outputs `cleaned_employee_data_csv.csv`

3. `clean_employee_data_fixed.py` - Enhanced csv module version
   - Adds BOM handling with UTF-8-SIG encoding
   - Improved error handling and preview display
   - Outputs `cleaned_employee_data_fixed.csv`

**Usage:**
```bash
python clean_employee_data.py
python clean_employee_data_csv.py
python clean_employee_data_fixed.py
```

All scripts expect `dirty_employee_data.csv` as input and produce cleaned output files with descriptive names.

## DNS Repair Tools

Scripts to fix GitHub DNS issues on Windows:

- `fix_github_dns.ps1` - PowerShell script (requires admin rights)
- `fix_github_dns.bat` - Batch file alternative
- `replace_hosts_admin.bat` - Replaces hosts file with `new_hosts.txt`
- `new_hosts.txt` - Pre-configured hosts file with GitHub IPs

**Important:** These scripts modify system files and require administrator privileges.

## Claude Code Skills

Custom skills located in `.claude/skills/`:

- `first` - Simple skill for testing the skill system
- `api-conventions` - API design guidelines for RESTful services
- `write` - Incomplete skill (placeholder)

Skills can be invoked via the Skill tool when relevant to the task.

## Content Files

- `微信公众号文章_资治通鉴视角的灰暗期启示.md` - WeChat public account article on coping with difficult periods using historical wisdom

## Development Notes

- No package dependencies are declared; pandas is used but not in a requirements file
- Scripts are standalone and can be run independently
- All output files are created in the repository root
- Chinese text handling with UTF-8 encoding throughout

When modifying scripts, maintain the existing structure and add comments in Chinese or English as appropriate.