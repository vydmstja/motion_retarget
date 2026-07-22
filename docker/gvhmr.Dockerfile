FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    git \
    ffmpeg \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools wheel

WORKDIR /workspace/GVHMR

# The source repository is bind-mounted at runtime. Install dependencies here so
# rebuilding is not needed when scripts or inputs change.
COPY repos/GVHMR/requirements.txt /tmp/gvhmr_requirements.txt
RUN python3 -m pip install --no-cache-dir numpy==1.23.5 && \
    python3 -m pip install --no-cache-dir --no-build-isolation chumpy==0.70 && \
    grep -v '^chumpy' /tmp/gvhmr_requirements.txt > /tmp/gvhmr_requirements_no_chumpy.txt && \
    python3 -m pip install --no-cache-dir -r /tmp/gvhmr_requirements_no_chumpy.txt

CMD ["bash"]
