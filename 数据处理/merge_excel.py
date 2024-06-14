# 将csv表全部合并为一个
import os
import pandas as pd


def merge_csv_files(input_folder, output_file):
    # 获取文件夹中所有 CSV 文件的路径
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # 创建一个空的 DataFrame 用于存储合并后的数据
    combined_df = pd.DataFrame()

    # 遍历所有 CSV 文件并合并
    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # 将合并后的数据写入新的 CSV 文件
    combined_df.to_csv(output_file, index=False)
    print("success")


# 示例用法
input_folder_in = 'D:/WORK/大三下/影评项目预测/爬取到的数据/合并处理'  # 替换为你的 CSV 文件夹路径
output_file = 'D:/WORK/大三下/影评项目预测/数据处理/all_movie_one_year.csv'  # 替换为你想要保存的输出文件名
merge_csv_files(input_folder_in, output_file)
