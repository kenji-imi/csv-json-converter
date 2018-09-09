# !/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import json
import sys
import traceback


def convert_json_to_csv(input_path, output_path, field_name):
    # JSONファイルのロード
    json_dict = json.load(open(input_path, 'r', encoding='utf-8'))

    # list of dictの抽出
    target_dicts = json_dict[field_name]

    with open(output_path, 'w', encoding='utf-8') as f:
        # dialectの登録
        csv.register_dialect('dialect01', doublequote=False)
        # DictWriter作成
        writer = csv.DictWriter(f, fieldnames=target_dicts[0].keys(), dialect='dialect01')
        # CSVへの書き込み
        writer.writeheader()
        for target_dict in target_dicts:
            writer.writerow(target_dict)


def convert_csv_to_json(input_path, output_path, field_name):
    json_list = []
    json_data = {}

    # CSVファイルのロード
    with open(input_path, 'r') as f:
        # list of dictの作成
        for line in csv.DictReader(f):
            json_list.append(line)

        json_data[field_name] = json_list

    with open(output_path, 'w') as f:
        # JSONへの書き込み
        json.dump(json_data, f, ensure_ascii=False)


def row_count(filename):
    with open(filename) as f:
        return sum(1 for _ in f)


def main():
    try:
        parser = argparse.ArgumentParser(description='file converter')
        parser.add_argument('--input_file', '-i', default="", help='input file')
        parser.add_argument('--output_file', '-o', default="", help='output file')
        parser.add_argument('--field_name', '-f', default="", help='field name')
        args = parser.parse_args()

        input_path = args.input_file  # data/xxx.json or data/xxx.csv
        output_path = args.output_file  # out/yyy.csv or out/yyy.json
        field_name = args.field_name  # 'cities'

        print("Start.")

        if len(input_path) == 0 or len(output_path) == 0 or len(field_name) == 0:
            print("invalid parameter")
            return

        if input_path[-4:] == "json":
            convert_json_to_csv(input_path, output_path, field_name)
        elif input_path[-3:] == "csv":
            convert_csv_to_json(input_path, output_path, field_name)
        else:
            print("invalid input file type")

        print("End.")

    except Exception as e:
        # print(e)
        # エラーの情報をsysモジュールから取得
        info = sys.exc_info()
        # tracebackモジュールのformat_tbメソッドで特定の書式に変換
        tbinfo = traceback.format_tb(info[2])

        # 収集した情報を読みやすいように整形して出力する
        # ----------------------------------
        print('Python Error.'.ljust(80, '='))
        for tbi in tbinfo:
            print(tbi)
        print('  %s' % str(info[1]))
        print('\n'.rjust(80, '='))
        # ----------------------------------


if __name__ == '__main__':
    main()
