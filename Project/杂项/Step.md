### 步骤 1: 安装 Microsoft C++ Build Tools
首先，确保你已经安装了 Microsoft C++ Build Tools，以确保某些包能够正确编译和安装。如果没有安装，可以从 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 下载并安装。安装过程中，确保选择“C++ 生成工具”（C++ build tools）。

### 步骤 2: 更新 `environment.txt` 文件
根据 `Readme.md` 文件中的包版本要求，并确保这些版本与 Python 3.12 兼容。以下是更新后的 `environment.txt` 文件内容，保留了未修改的部分，并更新了不兼容的包版本：

```plaintext
absl-py==1.4.0
async-generator==1.10
backcall==0.1.0
certifi==2021.5.30
cffi==1.15.1  # 更新到兼容版本
cloudpickle==1.6.0
colorama==0.4.1
cycler==0.10.0
decorator==4.4.0
future==0.18.2
gast==0.3.3
grpcio==1.23.0
hyperopt==0.2.5
Jinja2==2.11.3  # 更新到兼容版本
joblib==0.11
kiwisolver==1.3.1
Markdown==3.2.1
MarkupSafe==1.1.1
matplotlib==3.6.0  # 更新到兼容版本
mkl-fft==1.3.1  # 更新到兼容版本
mkl-random==1.2.2  # 更新到兼容版本
mkl-service==2.3.0
networkx==2.8.0  # 更新到兼容版本
numba==0.57.0  # 更新到兼容版本
numpy==1.21.0  # 更新到兼容版本
olefile==0.46
pandas==1.5.0  # 更新到兼容版本
pickleshare==0.7.5
Pillow==8.1.2
protobuf==3.20.0  # 更新到兼容版本
pycairo==1.19.1
pycparser==2.21  # 更新到兼容版本
Pygments==2.8.2
pyparsing==3.0.10  # 更新到兼容版本
pyreadline3  # 替换为 pyreadline3
python-dateutil==2.8.0
pytz==2019.2
pywin32==223
pywinpty==0.5.7
PyYAML==5.1.2
pyzmq==18.1.0
rdkit==2023.09.3  # 更新到兼容版本
scikit-learn==1.2.2  # 更新到兼容版本
scipy==1.10.1  # 更新到兼容版本
six==1.16.0  # 更新到兼容版本
tensorboard==2.15.0  # 更新到兼容版本
tensorflow==2.12.0  # 更新到兼容版本
tensorflow-estimator==2.12.0  # 更新到兼容版本
termcolor==1.1.0
terminado==0.16.3  # 更新到兼容版本
torch==2.0.1  # 更新到兼容版本
torchvision==0.15.1  # 更新到兼容版本
tornado==6.3.1  # 更新到兼容版本
Werkzeug==2.3.7  # 更新到兼容版本
```

### 步骤 3: 保存修改后的 `environment.txt` 文件
将上述修改后的内容保存到 `environment.txt` 文件中。

### 步骤 4: 更新 `train.py` 文件中的导入路径
根据 `Readme.md` 文件中的说明，`train.py` 文件中的导入路径可能会有问题。你需要确保 `train.py` 文件中的导入路径正确。以下是示例修改：

```python
# train.py
from FPGNN.fpgnn.train import fold_train
```

确保 `FPGNN` 文件夹在项目的正确路径下，并且包含 `__init__.py` 文件。

### 步骤 5: 安装依赖项
在虚拟环境中运行以下命令来安装依赖项：

```bash
# 激活虚拟环境（假设虚拟环境名为 myenv）
myenv\Scripts\activate

# 安装依赖项
pip install -r E:\VSCode\Coding\Project\FPGNN\environment.txt
```

### 步骤 6: 运行训练命令
根据 `Readme.md` 文件中的说明，训练模型的命令如下：

```bash
python train.py --data_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --dataset_type classification --save_path E:\VSCode\Coding\Project\FPGNN\model_save --log_path E:\VSCode\Coding\Project\FPGNN\log
```

### 步骤 7: 运行预测命令
训练完成后，使用以下命令进行预测：

```bash
python predict.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --result_path E:\VSCode\Coding\Project\FPGNN\result.csv
```

### 步骤 8: 运行超参数优化命令
如果需要进行超参数优化，使用以下命令：

```bash
python hyper_opti.py --data_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --dataset_type classification --save_path E:\VSCode\Coding\Project\FPGNN\model_save --log_path E:\VSCode\Coding\Project\FPGNN\log
```

### 步骤 9: 运行指纹解释命令
如果需要解释指纹，使用以下命令：

```bash
python interpretation_fp.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --result_path E:\VSCode\Coding\Project\FPGNN\result.txt
```

### 步骤 10: 运行分子图解释命令
如果需要解释分子图，使用以下命令：

```bash
python interpretation_graph.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --figure_path E:\VSCode\Coding\Project\FPGNN\figure
```

### 完整的 `environment.txt` 文件内容

以下是完整的修改后的 `environment.txt` 文件内容：

```plaintext
absl-py==1.4.0
async-generator==1.10
backcall==0.1.0
certifi==2021.5.30
cffi==1.15.1
cloudpickle==1.6.0
colorama==0.4.1
cycler==0.10.0
decorator==4.4.0
future==0.18.2
gast==0.3.3
grpcio==1.23.0
hyperopt==0.2.5
Jinja2==2.11.3
joblib==0.11
kiwisolver==1.3.1
Markdown==3.2.1
MarkupSafe==1.1.1
matplotlib==3.6.0
mkl-fft==1.3.1
mkl-random==1.2.2
mkl-service==2.3.0
networkx==2.8.0
numba==0.57.0
numpy==1.21.0
olefile==0.46
pandas==1.5.0
pickleshare==0.7.5
Pillow==8.1.2
protobuf==3.20.0
pycairo==1.19.1
pycparser==2.21
Pygments==2.8.2
pyparsing==3.0.10
pyreadline3
python-dateutil==2.8.0
pytz==2019.2
pywin32==223
pywinpty==0.5.7
PyYAML==5.1.2
pyzmq==18.1.0
rdkit==2023.09.3
scikit-learn==1.2.2
scipy==1.10.1
six==1.16.0
tensorboard==2.15.0
tensorflow==2.12.0
tensorflow-estimator==2.12.0
termcolor==1.1.0
terminado==0.16.3
torch==2.0.1
torchvision==0.15.1
tornado==6.3.1
Werkzeug==2.3.7
```

### 安装 Microsoft C++ Build Tools
确保你已经安装了 Microsoft C++ Build Tools。如果没有安装，可以从 [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 下载并安装。安装过程中，确保选择“C++ 生成工具”（C++ build tools）。

### 安装依赖项
再次运行以下命令来安装依赖项：

```bash
# 激活虚拟环境
myenv\Scripts\activate

# 安装依赖项
pip install -r E:\VSCode\Coding\Project\FPGNN\environment.txt
```

### 运行项目
按照以下步骤运行项目：

1. **训练模型**：
   ```bash
   python train.py --data_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --dataset_type classification --save_path E:\VSCode\Coding\Project\FPGNN\model_save --log_path E:\VSCode\Coding\Project\FPGNN\log
   ```

2. **使用模型进行预测**：
   ```bash
   python predict.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --result_path E:\VSCode\Coding\Project\FPGNN\result.csv
   ```

3. **超参数优化**：
   ```bash
   python hyper_opti.py --data_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --dataset_type classification --save_path E:\VSCode\Coding\Project\FPGNN\model_save --log_path E:\VSCode\Coding\Project\FPGNN\log
   ```

4. **解释指纹**：
   ```bash
   python interpretation_fp.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --result_path E:\VSCode\Coding\Project\FPGNN\result.txt
   ```

5. **解释分子图**：
   ```bash
   python interpretation_graph.py --predict_path E:\VSCode\Coding\Project\FPGNN\data/test.csv --model_path E:\VSCode\Coding\Project\FPGNN\model_save/Seed_0/model.pt --figure_path E:\VSCode\Coding\Project\FPGNN\figure
   ```
