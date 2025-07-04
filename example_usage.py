#!/usr/bin/env python3
"""
Example usage of the Comment Watcher with different configurations.
This demonstrates how to use the modular structure for different use cases.
"""

from comment_watcher import CommentWatcher
from comment_analyzer import CommentAnalyzer
from config import Config

def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    watcher = CommentWatcher()
    results = watcher.run_monitoring_cycle()
    return results

def example_custom_keywords():
    """Example with custom keywords."""
    print("\n=== Custom Keywords Example ===")

    # Create watcher with custom analyzer
    custom_keywords = ["climate", "emissions", "carbon"]
    analyzer = CommentAnalyzer(keywords=custom_keywords)

    # Create watcher with custom analyzer
    watcher = CommentWatcher()
    watcher.analyzer = analyzer

    results = watcher.run_monitoring_cycle(page_size=10)
    return results

def example_larger_batch():
    """Example with larger batch size."""
    print("\n=== Larger Batch Example ===")
    watcher = CommentWatcher()
    results = watcher.run_monitoring_cycle(page_size=50)
    return results

def example_view_history():
    """Example of viewing historical data."""
    print("\n=== Historical Data Example ===")
    watcher = CommentWatcher()
    historical = watcher.get_historical_data()

    print(f"📚 Found {len(historical)} historical flagged comments")
    for comment in historical[:3]:  # Show first 3
        print(f"  - {comment['title'][:50]}... (matched: {comment['keyword']})")

    return historical

def main():
    """Run all examples."""
    print("🚀 Comment Watcher Examples")
    print("=" * 50)

    # Run examples
    basic_results = example_basic_usage()
    custom_results = example_custom_keywords()
    large_results = example_larger_batch()
    history = example_view_history()

    # Summary
    print("\n" + "=" * 50)
    print("📊 EXAMPLE SUMMARY:")
    print(f"  Basic run: {basic_results['flagged_count']} flagged")
    print(f"  Custom keywords: {custom_results['flagged_count']} flagged")
    print(f"  Large batch: {large_results['flagged_count']} flagged")
    print(f"  Historical data: {len(history)} total saved")

if __name__ == "__main__":
    main()
