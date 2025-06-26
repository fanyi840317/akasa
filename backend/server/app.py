# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import sys
from pathlib import Path
backend_path = str((Path(__file__).parent.parent).resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from server.routes import audio, chat, config, generation, mcp

logger = logging.getLogger(__name__)

app = FastAPI(
    title="DeerFlow API",
    description="API for Deer",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(chat.router)
app.include_router(audio.router)
app.include_router(generation.router)
app.include_router(mcp.router)
app.include_router(config.router)
