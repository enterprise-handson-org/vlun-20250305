# long_functions_example.py

import os
import sys
import json
import datetime
import random
import math
from typing import List, Dict, Any, Optional, Tuple

def short_function(n: int) -> int:
    """この関数は短いので問題ありません"""
    return n * 2

def very_long_function(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    この関数は故意に長く作られており、CodeQL の long_functions.ql に検出されるはずです。
    この関数は50行以上になるため、リファクタリングの対象になるでしょう。
    """
    result = {}
    processed_items = 0
    error_count = 0
    warnings = []
    
    # 初期チェック
    if not data:
        print("No data provided")
        return {"error": "No data provided"}
    
    # データの処理開始
    for item in data:
        # 各項目をチェック
        if "id" not in item:
            warnings.append(f"Missing ID in item {processed_items}")
            continue
            
        # IDの検証
        if not isinstance(item["id"], (int, str)):
            warnings.append(f"Invalid ID type for item {processed_items}: {type(item['id'])}")
            continue
            
        # 名前の検証
        if "name" not in item:
            warnings.append(f"Missing name in item {item['id']}")
            item["name"] = f"Unknown_{item['id']}"
        
        # 日付のチェックとフォーマット
        if "date" in item:
            try:
                date_obj = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
                item["formatted_date"] = date_obj.strftime("%d %B %Y")
            except ValueError:
                warnings.append(f"Invalid date format in item {item['id']}")
                item["formatted_date"] = "Unknown date"
        
        # 複雑な計算 1
        if "values" in item and isinstance(item["values"], list):
            total = sum(item["values"])
            average = total / len(item["values"]) if item["values"] else 0
            maximum = max(item["values"]) if item["values"] else 0
            minimum = min(item["values"]) if item["values"] else 0
            
            # 標準偏差の計算
            squared_diff_sum = sum((x - average) ** 2 for x in item["values"]) if item["values"] else 0
            std_dev = math.sqrt(squared_diff_sum / len(item["values"])) if item["values"] else 0
            
            item["stats"] = {
                "total": total,
                "average": average,
                "max": maximum,
                "min": minimum,
                "std_dev": std_dev
            }
        
        # 複雑な処理 2
        if "tags" in item and isinstance(item["tags"], list):
            # タグの重複を除去
            unique_tags = list(set(item["tags"]))
            
            # タグの頻度を数える
            tag_frequency = {}
            for tag in item["tags"]:
                if tag in tag_frequency:
                    tag_frequency[tag] += 1
                else:
                    tag_frequency[tag] = 1
            
            # 最も頻度の高いタグを見つける
            most_common_tag = max(tag_frequency.items(), key=lambda x: x[1])[0] if tag_frequency else None
            
            item["tag_analysis"] = {
                "unique_count": len(unique_tags),
                "most_common": most_common_tag,
                "frequencies": tag_frequency
            }
        
        # リソースの使用状況をチェック
        memory_usage = sys.getsizeof(item) / 1024  # KB単位
        if memory_usage > 100:  # 100KB以上の場合は警告
            warnings.append(f"Item {item['id']} is using {memory_usage:.2f}KB of memory")
        
        # 処理された項目をカウント
        processed_items += 1
        
        # 結果に追加
        result[item["id"]] = item
    
    # 最終的な統計情報
    result["_metadata"] = {
        "processed_count": processed_items,
        "error_count": error_count,
        "warning_count": len(warnings),
        "warnings": warnings,
        "processing_time": datetime.datetime.now().isoformat(),
        "memory_usage": sum(sys.getsizeof(item) for item in data) / 1024 if data else 0
    }
    
    # 完了メッセージ
    print(f"Processed {processed_items} items with {len(warnings)} warnings")
    
    return result

def another_long_function() -> None:
    """
    これは別の長い関数の例です。
    この関数も50行を超えるためCodeQLに検出されるでしょう。
    """
    # 大きなデータセットの初期化
    large_dataset = []
    for i in range(1000):
        large_dataset.append({
            "id": i,
            "value": random.random(),
            "name": f"Item_{i}",
            "is_active": random.choice([True, False]),
            "created_at": datetime.datetime.now().isoformat()
        })
    
    # データのフィルタリング
    filtered_items = []
    for item in large_dataset:
        if item["value"] > 0.5 and item["is_active"]:
            filtered_items.append(item)
    
    # データの集計
    total_value = 0
    active_count = 0
    inactive_count = 0
    
    for item in large_dataset:
        total_value += item["value"]
        if item["is_active"]:
            active_count += 1
        else:
            inactive_count += 1
    
    # 複雑な処理1
    value_distribution = {}
    for i in range(10):
        lower = i / 10
        upper = (i + 1) / 10
        count = sum(1 for item in large_dataset if lower <= item["value"] < upper)
        value_distribution[f"{lower:.1f}-{upper:.1f}"] = count
    
    # 複雑な処理2
    id_clusters = {}
    for item in large_dataset:
        cluster = item["id"] // 100
        if cluster not in id_clusters:
            id_clusters[cluster] = []
        id_clusters[cluster].append(item)
    
    # クラスタごとの統計
    cluster_stats = {}
    for cluster, items in id_clusters.items():
        avg_value = sum(item["value"] for item in items) / len(items)
        active_ratio = sum(1 for item in items if item["is_active"]) / len(items)
        cluster_stats[cluster] = {
            "count": len(items),
            "avg_value": avg_value,
            "active_ratio": active_ratio
        }
    
    # 結果の出力
    print(f"Total items: {len(large_dataset)}")
    print(f"Active items: {active_count}")
    print(f"Inactive items: {inactive_count}")
    print(f"Average value: {total_value / len(large_dataset):.4f}")
    print(f"Filtered items: {len(filtered_items)}")
    
    print("\nValue distribution:")
    for range_label, count in value_distribution.items():
        print(f"  {range_label}: {count}")
    
    print("\nCluster statistics:")
    for cluster, stats in cluster_stats.items():
        print(f"  Cluster {cluster}: {stats['count']} items, " + 
              f"avg value: {stats['avg_value']:.4f}, " + 
              f"active ratio: {stats['active_ratio']:.2f}")
    
    # データの保存
    with open("analysis_results.json", "w") as f:
        json.dump({
            "total_items": len(large_dataset),
            "active_count": active_count,
            "inactive_count": inactive_count,
            "avg_value": total_value / len(large_dataset),
            "filtered_count": len(filtered_items),
            "value_distribution": value_distribution,
            "cluster_stats": cluster_stats
        }, f, indent=2)
    
    print("Analysis complete. Results saved to analysis_results.json")


if __name__ == "__main__":
    # サンプルデータ
    sample_data = [
        {"id": 1, "name": "Item 1", "values": [10, 20, 30], "tags": ["a", "b", "a"]},
        {"id": 2, "name": "Item 2", "values": [5, 15, 25], "tags": ["b", "c"]},
        {"id": 3, "date": "2023-01-15", "values": [7, 14, 21]}
    ]
    
    # 長い関数を呼び出す
    result = very_long_function(sample_data)
    print(json.dumps(result, indent=2))
    
    # もう一つの長い関数を呼び出す
    another_long_function()
