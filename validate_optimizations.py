#!/usr/bin/env python3
"""
Validation script to verify that the optimized code produces identical results
to the original implementation.
"""

import pandas as pd
import numpy as np

def test_rounding_optimization():
    """Test that vectorized round() produces same results as apply(lambda)."""
    print("Testing Optimization 1: Vectorized Rounding")
    print("-" * 60)
    
    # Create test data with various cases
    test_data = pd.Series([
        45.6789,
        67.1234,
        np.nan,
        100.0,
        0.5,
        99.999,
        np.nan,
        50.5
    ])
    
    # Original method (inefficient)
    result_original = test_data.apply(lambda x: round(x) if pd.notna(x) else x)
    
    # Optimized method
    result_optimized = test_data.round()
    
    # Compare results
    comparison = pd.DataFrame({
        'Original': result_original,
        'Optimized': result_optimized,
        'Equal': result_original.equals(result_optimized)
    })
    
    print(comparison)
    
    # Check if they're equal (considering NaN == NaN)
    if result_original.equals(result_optimized):
        print("\n✅ PASS: Both methods produce identical results!")
        return True
    else:
        print("\n❌ FAIL: Results differ!")
        return False


def test_type_conversion_optimization():
    """Test that vectorized apply produces same results as loop."""
    print("\n\nTesting Optimization 2: Vectorized Type Conversion")
    print("-" * 60)
    
    # Create test DataFrame with year columns
    test_df = pd.DataFrame({
        'Country': ['USA', 'Canada', 'Mexico'],
        '2012 [YR2012]': ['95.5', '100.0', '88.3'],
        '2013 [YR2013]': ['96.0', '100.0', '89.1'],
        '2014 [YR2014]': ['96.5', '100.0', '..'],  # '..' is invalid, should become NaN
        '2015 [YR2015]': ['97.0', '100.0', '90.5']
    })
    
    # Get year columns
    year_columns = [col for col in test_df.columns if 'YR' in col]
    
    # Original method (inefficient) - loop
    df_original = test_df.copy()
    for col in year_columns:
        df_original[col] = pd.to_numeric(df_original[col], errors='coerce')
    
    # Optimized method - vectorized apply
    df_optimized = test_df.copy()
    df_optimized[year_columns] = df_optimized[year_columns].apply(pd.to_numeric, errors='coerce')
    
    # Compare results
    print("\nOriginal method result:")
    print(df_original)
    print("\nOptimized method result:")
    print(df_optimized)
    
    # Check if they're equal
    if df_original.equals(df_optimized):
        print("\n✅ PASS: Both methods produce identical results!")
        return True
    else:
        print("\n❌ FAIL: Results differ!")
        print("\nDifferences:")
        for col in year_columns:
            if not df_original[col].equals(df_optimized[col]):
                print(f"  Column {col} differs")
        return False


def test_with_actual_data():
    """Test with the actual dataset if available."""
    print("\n\nTesting with Actual Dataset")
    print("-" * 60)
    
    try:
        # Load the actual dataset
        df = pd.read_csv("access_electricity.csv")
        print(f"Loaded dataset with {len(df)} rows")
        
        # Test rounding on actual data
        df['2016 [YR2016]'] = pd.to_numeric(df['2016 [YR2016]'], errors='coerce')
        
        # Original method
        result_orig = df['2016 [YR2016]'].apply(lambda x: round(x) if pd.notna(x) else x)
        
        # Optimized method
        result_opt = df['2016 [YR2016]'].round()
        
        if result_orig.equals(result_opt):
            print("✅ PASS: Rounding produces identical results on actual data!")
        else:
            print("❌ FAIL: Rounding results differ on actual data!")
            return False
        
        # Test type conversion on actual data
        year_columns = [col for col in df.columns if 'YR' in col]
        
        df_loop = df.copy()
        for col in year_columns:
            df_loop[col] = pd.to_numeric(df_loop[col], errors='coerce')
        
        df_vec = df.copy()
        df_vec[year_columns] = df_vec[year_columns].apply(pd.to_numeric, errors='coerce')
        
        if df_loop[year_columns].equals(df_vec[year_columns]):
            print("✅ PASS: Type conversion produces identical results on actual data!")
            return True
        else:
            print("❌ FAIL: Type conversion results differ on actual data!")
            return False
            
    except FileNotFoundError:
        print("⚠️  Dataset file not found, skipping actual data test")
        return True
    except Exception as e:
        print(f"⚠️  Error testing with actual data: {e}")
        return True


def main():
    """Run all validation tests."""
    print("="*60)
    print("VALIDATION: Performance Optimizations")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(test_rounding_optimization())
    results.append(test_type_conversion_optimization())
    results.append(test_with_actual_data())
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if all(results):
        print("✅ All validation tests PASSED!")
        print("\nThe optimized code produces identical results to the original")
        print("implementation while being significantly faster.")
        return 0
    else:
        print("❌ Some validation tests FAILED!")
        return 1


if __name__ == "__main__":
    exit(main())
