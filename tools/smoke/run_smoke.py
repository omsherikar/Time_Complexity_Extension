import os
import sys
from typing import List, Dict

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(PROJECT_ROOT)

from ml_integration.hybrid_analyzer import HybridTimeComplexityAnalyzer


def get_test_cases() -> List[Dict]:
    return [
        # C++ Matrix Chain Multiplication DP (expect O(n³), O(n²))
        {
            'name': 'C++ Matrix Chain Multiplication DP',
            'language': 'cpp',
            'expected_time': 'O(n³)',
            'expected_space': 'O(n²)',
            'code': r'''
int MatrixChainOrder(int p[], int n) {
    int m[n][n];
    int i, j, k, L, q;
    for (i = 1; i < n; i++) m[i][i] = 0;
    for (L = 2; L < n; L++) {
        for (i = 1; i < n - L + 1; i++) {
            j = i + L - 1;
            m[i][j] = 1e9;
            for (k = i; k <= j - 1; k++) {
                q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j];
                if (q < m[i][j]) m[i][j] = q;
            }
        }
    }
    return m[1][n-1];
}
'''
        },
        # C++ Merge Sort (expect O(n log n), O(n))
        {
            'name': 'C++ Merge Sort',
            'language': 'cpp',
            'expected_time': 'O(n log n)',
            'expected_space': 'O(n)',
            'code': r'''
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
'''
        },
        # C++ Bubble Sort (expect O(n²), O(1))
        {
            'name': 'C++ Bubble Sort',
            'language': 'cpp',
            'expected_time': 'O(n²)',
            'expected_space': 'O(1)',
            'code': r'''
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int t = arr[j]; arr[j] = arr[j+1]; arr[j+1] = t;
            }
        }
    }
}
'''
        },
        # C++ Binary Search (expect O(log n), O(1))
        {
            'name': 'C++ Binary Search',
            'language': 'cpp',
            'expected_time': 'O(log n)',
            'expected_space': 'O(1)',
            'code': r'''
int binarySearch(int arr[], int l, int r, int x) {
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (arr[mid] == x) return mid;
        if (arr[mid] < x) l = mid + 1; else r = mid - 1;
    }
    return -1;
}
'''
        },
        # Java permutations backtracking (expect O(n!), O(n))
        {
            'name': 'Java Permutations Backtracking',
            'language': 'java',
            'expected_time': 'O(n!)',
            'expected_space': 'O(n)',
            'code': r'''
import java.util.*;
class Solution {
  void permute(int[] nums, int l) {
    if (l == nums.length) return;
    for (int i = l; i < nums.length; i++) {
      int t = nums[l]; nums[l] = nums[i]; nums[i] = t;
      permute(nums, l+1);
      t = nums[l]; nums[l] = nums[i]; nums[i] = t;
    }
  }
}
'''
        },
        # Java using TreeMap operations (expect O(n log n), O(n))
        {
            'name': 'Java TreeMap Ops in Loop',
            'language': 'java',
            'expected_time': 'O(n log n)',
            'expected_space': 'O(n)',
            'code': r'''
import java.util.*;
class Demo {
  void f(List<Integer> a) {
    TreeMap<Integer, Integer> t = new TreeMap<>();
    for (int x : a) {
      t.put(x, t.getOrDefault(x, 0) + 1);
    }
  }
}
'''
        },
        # Python Fibonacci recursion (O(2^n), O(n))
        {
            'name': 'Python Fibonacci Recursive',
            'language': 'python',
            'expected_time': 'O(2ⁿ)',
            'expected_space': 'O(n)',
            'code': r'''
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
'''
        },
        # Python Merge Sort (O(n log n), O(n))
        {
            'name': 'Python Merge Sort',
            'language': 'python',
            'expected_time': 'O(n log n)',
            'expected_space': 'O(n)',
            'code': r'''
def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a)//2
    L = merge_sort(a[:m])
    R = merge_sort(a[m:])
    i=j=0
    out=[]
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    out.extend(L[i:]); out.extend(R[j:])
    return out
'''
        },
        # JS array sort (O(n log n), O(1))
        {
            'name': 'JS Array.sort Comparator',
            'language': 'javascript',
            'expected_time': 'O(n log n)',
            'expected_space': 'O(1)',
            'code': r'''
function s(arr){ return arr.sort((a,b)=>a-b); }
'''
        },
        # C++ linear scan while (O(n), O(1))
        {
            'name': 'C++ Linear While Scan',
            'language': 'cpp',
            'expected_time': 'O(n)',
            'expected_space': 'O(1)',
            'code': r'''
int scan(int* a, int n, int x){ int i=0; while(i<n){ if(a[i]==x) return i; i++; } return -1; }
'''
        },
        # Java bubble sort (O(n²), O(1))
        {
            'name': 'Java Bubble Sort',
            'language': 'java',
            'expected_time': 'O(n²)',
            'expected_space': 'O(1)',
            'code': r'''
class B { void b(int[] a){ int n=a.length; for(int i=0;i<n-1;i++){ for(int j=0;j<n-i-1;j++){ if(a[j]>a[j+1]){ int t=a[j]; a[j]=a[j+1]; a[j+1]=t; } } } } }
'''
        },
    ]


def main():
    ml_path = os.path.join(PROJECT_ROOT, 'ml_integration', 'ml_models.pkl')
    analyzer = HybridTimeComplexityAnalyzer(ml_path if os.path.exists(ml_path) else None)

    total = 0
    correct = 0
    for tc in get_test_cases():
        total += 1
        res = analyzer.analyze(tc['code'], tc['language'])
        time_ok = tc['expected_time'] in res['time_complexity']
        space_ok = tc['expected_space'] in res['space_complexity']
        ok = time_ok and space_ok
        correct += 1 if ok else 0
        print(f"[{ 'PASS' if ok else 'FAIL' }] {tc['name']}")
        print(f"  Time:   {res['time_complexity']} (exp {tc['expected_time']})")
        print(f"  Space:  {res['space_complexity']} (exp {tc['expected_space']})")
        print(f"  Method: {res.get('analysis_method', 'n/a')}  Conf: {res.get('ensemble_confidence', 0):.2f}")
    print(f"\nScore: {correct}/{total} correct ({(100.0*correct/total):.1f}%)")


if __name__ == '__main__':
    main()
