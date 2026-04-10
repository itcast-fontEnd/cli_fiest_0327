#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图表模板项目安装配置
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chart-templates',
    version='1.1.0',
    description='可复用的数据可视化图表模板系统',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='数据分析团队',
    author_email='your-email@example.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'numpy>=1.21.0',
        'pandas>=1.3.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
        ],
        'advanced': [
            'scikit-learn>=1.0.0',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    project_urls={
        'Source': 'https://github.com/yourusername/chart-templates',
    },
)