The helper tool one can use to classify changes in a _git_ repository.

For a given set of changes, the tool analyses each modified file to check if changes introduce any new dependencies or capabilities.
The tool puts the files analyzed to category buckets according to non-formal description of the categories in plain English. E.g. "Invokes REST API", or "Accesses AWS S3".

It uses AI model for understanding semantics of category and analyzing the source code.

# Usage

Edit config.yaml to specify which AI model to use and what categories to use.

~~~sh
ai-classify-changes <repo-path> <git-diff-args>...
~~~

## Examples

* Changes in a commit, given by its sha1, to its parent:
~~~sh
ai-classify-changes some-path-1 f2cf816^!
~~~

* Changes between two tags:
~~~sh
ai-classify-changes some-path-2 v1.10.0 v1.11.0
~~~

* Ignore files in directories data and docs:
~~~sh
ai-classify-changes some-path-2 v1.10.0 v1.11.0 -- ':(exclude)data' ':(exclude)docs'
~~~

# A real-life example and how different models analyze same code samples

This demonstration uses this single commit in _github.com/odoo_ repository: https://github.com/odoo/odoo/commit/f2cf816

You can replicate the results if you execute following commands.
~~~sh
git clone https://github.com/MaksimAniskov/ai-classify-changes.git
pip3 install -r ai-classify-changes/requirements.txt

git clone https://github.com/odoo/odoo.git # !!! Attention! This repo is very heavy. It has some 12GB of stuff to download.

export OPENAI_API_KEY=...
./ai-classify-changes/ai-classify-changes odoo f2cf816^!
~~~

## Models comparison

| |gpt-5|gpt-5-min|gpt-5-nano|gpt-4.1|gpt-4.1-mini|gpt-4.1-nano|gpt-oss:20b|
|-|-----|---------|----------|-------|------------|------------|-----------|
|addons/cloud_storage/\_\_init\_\_.py||||||||
|addons/cloud_storage/\_\_manifest\_\_.py||||||||
|addons/cloud_storage/controllers/\_\_init\_\_.py||||||||
|addons/cloud_storage/controllers/attachment.py||Executes SQL query against relational database|||Invokes REST API|||
|addons/cloud_storage/data/neutralize.sql|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|
|addons/cloud_storage/models/\_\_init\_\_.py||||||||
|addons/cloud_storage/models/ir_attachment.py||Executes SQL query against relational database||||||
|addons/cloud_storage/models/ir_http.py|||||||Executes SQL query against relational database|
|addons/cloud_storage/models/res_config_settings.py||Executes SQL query against relational database||||||
|addons/cloud_storage/static/src/core/common/attachment_upload_service_patch.js|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|
|addons/cloud_storage/views/settings.xml||||||||
|addons/cloud_storage_azure/\_\_init\_\_.py|Executes SQL query against relational database|Executes SQL query against relational database|||||Executes SQL query against relational database|
|addons/cloud_storage_azure/\_\_manifest\_\_.py||||||||
|addons/cloud_storage_azure/data/neutralize.sql|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|
|addons/cloud_storage_azure/models/\_\_init\_\_.py||||||||
|addons/cloud_storage_azure/models/ir_attachment.py|Invokes REST API|Invokes REST API|Invokes REST API|||Invokes REST API||
|addons/cloud_storage_azure/models/res_config_settings.py,|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API|Invokes REST API, Executes SQL query against relational database|
|addons/cloud_storage_azure/tests/\_\_init\_\_.py||||||||
|addons/cloud_storage_azure/tests/test_cloud_storage_azure.py|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|
|addons/cloud_storage_azure/utils/\_\_init\_\_.py||||||||
|addons/cloud_storage_azure/utils/cleanup_cloud_storage_azure.py|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API, Executes SQL query against relational database|Invokes REST API|
|addons/cloud_storage_azure/utils/cloud_storage_azure_utils.py|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|
|addons/cloud_storage_azure/views/settings.xml||||||||
|addons/cloud_storage_google/\_\_init\_\_.py|Executes SQL query against relational database|Executes SQL query against relational database||||||
|addons/cloud_storage_google/\_\_manifest\_\_.py||||||||
|addons/cloud_storage_google/data/neutralize.sql|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|Executes SQL query against relational database|
|addons/cloud_storage_google/models/\_\_init\_\_.py||||||||
|addons/cloud_storage_google/models/ir_attachment.py||||||Invokes REST API||
|addons/cloud_storage_google/models/res_config_settings.py,|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|Invokes REST API, Executes SQL query against relational database|
|addons/cloud_storage_google/static/src/scss/cloud_storage_google.scss||||||||
|addons/cloud_storage_google/tests/\_\_init\_\_.py||||||||
|addons/cloud_storage_google/tests/test_cloud_storage_google.py||Executes SQL query against relational database|||Invokes REST API|Invokes REST API||
|addons/cloud_storage_google/utils/\_\_init\_\_.py||||||||
|addons/cloud_storage_google/utils/cleanup_cloud_storage_google.py|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API, Executes SQL query against relational database|Invokes REST API|
|addons/cloud_storage_google/utils/cloud_storage_google_utils.py||||||Invokes REST API||
|addons/cloud_storage_google/views/settings.xml||||||||
|addons/mail/static/src/core/common/attachment_upload_service.js|||||Invokes REST API|||
|addons/mail/static/src/discuss/voice_message/common/attachment_uploader_hook_patch.js||||||||
|odoo/addons/base/models/ir_attachment.py||||||||
|odoo/addons/base/models/ir_binary.py||||||||
|odoo/addons/base/models/ir_http.py|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API|Invokes REST API||
|odoo/http.py|||||Invokes REST API|Invokes REST API||
