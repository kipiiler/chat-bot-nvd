# **NVD Bot – CVE Query Assistant**  

## **Overview**  
NVD Bot is an AI-powered assistant designed to help you query CVEs (Common Vulnerabilities and Exposures) from the [National Vulnerability Database (NVD)](https://nvd.nist.gov/). It supports filtering vulnerabilities by keyword, date, severity, and affected products using CPE (Common Platform Enumeration).  

---

## **Setup Instructions**  

### **1. Configure API Keys**  
Before running the bot, set up your environment variables for OpenAI or vLLM and the NVD API:  

```sh
export OPENAI_API_KEY=<your_openai_key>
export NVD_API_KEY=<your_nvd_key>
```

Alternatively, you can add these to an `env.sh` file and source it:  

```sh
source env.sh
```

### **2. Running with vLLM (Optional)**  
If using `vLLM` instead of OpenAI, start the model server with DeepSeek or LLaMA:  

```sh
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-14B \
    --gpu-memory-utilization=0.94 \
    --enable-chunked-prefill \
    --max-model-len=56000 \
    --enable-reasoning \
    --reasoning-parser deepseek_r1
```

### **3. Install Dependencies**  
Ensure required dependencies are installed:  

```sh
pip install -r requirements.txt
```

### **4. Start the Chatbot**  
Run the bot:  

```sh
python main.py
```

---

## **Example Queries**  

### **🔹 Basic CVE Queries**  
- _"What is CVE-2023-12345?"_  
- _"Can you explain the impact of CVE-2024-47195?"_  
- _"How severe is CVE-2022-67890?"_  
- _"Is there a patch available for CVE-2021-99999?"_  

### **🔹 Search by keyword**
-  _"What is spectre attack"_
-  _"Were there any OpenSSL vulnerabilities in January of 2024?"_

### **🔹 Filtering and Searching**  
- _"Show me recent CVEs related to OpenSSL."_  
- _"Find vulnerabilities in Windows reported in 2023."_  
- _"List all high-severity CVEs for Linux Kernel."_  

