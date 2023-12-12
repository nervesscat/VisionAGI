![Banner](https://i.imgur.com/X1VQkTw.png)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nervesscat)

<span style="color: orange; font-size: 1.5em;">**This is a non-finished proyect, if you want to collaborate, don't be afraid and contact with me :D**</span>

# VisionGPT - Introduction
VisionGPT is an **AutoGPT** this model speaks with itself in order to achieve a goal, this will be everything that can be replicated in a computer. This model use a combination of **GPT-3.5 Turbo**, **GPT-4** and **GPT-V** models.

# Installation

## Virtual Environment (<span style="color: green;">Optional</span>)

Create a virtual environment using venv:

### Install venv:
```bash
sudo apt install python3-venv
```

### Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Set the environment variables:

If you use a virtual environment, you need to set the environment variables in the file **.env**:

```bash
export OPENAI_API_KEY=YOUR_API_KEY
```

If you don't use a virtual environment, you need to set the environment variables in the system, for [Linux](https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/) and for [Windows](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).

## Install the requirements:

```bash
pip install -r requirements.txt
```

## Run the program:

```bash
python3 main.py
```

# How to use
At the beginning of the script, you'll have to write a prompt, this prompt should be the goal that you want to achieve, for example:

```bash 
> Open facebook
```