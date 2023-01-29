cloudflare-agent-qa
===================

This is a small langchain hello-world toy application, that answers questions about the cloudflare development documentation.

I've indexed the cloudflare documentation markdown files, [located here](https://github.com/cloudflare/cloudflare-docs/tree/production/content), into a FAISS store.


### Asking a question

This repo includes the vector store, and index, which means you too can ask questions:

```
python qa.py "Can you summarize how to setup email routing, in 5 steps?"

answer: To setup email routing, the following 5 steps should be followed: 1) Log in to the Cloudflare dashboard and select your account and domain; 2) Go to Email > Email Routing and select Get started; 3) Enter the custom email address you want to use in Custom address; 4) Enter the full email address you want your emails to be forwarded to in Destination address; 5) Select Create and continue
```