import json
import os
from typing import List, Dict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATASET_PATH = os.path.join(PROJECT_ROOT, 'ml_integration', 'ml_dataset.json')


def samples() -> List[Dict]:
    out: List[Dict] = []

    def rec(code: str, language: str, time: str, space: str, algo: str):
        return {
            'code': code.strip('\n'),
            'language': language,
            'time_complexity': time,
            'space_complexity': space,
            'algorithm_type': algo,
            'patterns': [],
            'confidence': 0.95,
            'source': 'canonical'
        }

    # C++ O(1)
    out.append(rec(r'''int getFirst(const std::vector<int>& a){ return a[0]; }''', 'cpp', 'O(1)', 'O(1)', 'constant'))
    # C++ O(log n) binary search
    out.append(rec(r'''int bs(std::vector<int>& a,int x){int l=0,r=a.size()-1;while(l<=r){int mid=l+(r-l)/2; if(a[mid]==x) return mid; if(a[mid]<x) l=mid+1; else r=mid-1;}return -1;}''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    # C++ O(n)
    out.append(rec(r'''int sum(std::vector<int>& a){int s=0; for(int x: a) s+=x; return s;}''', 'cpp', 'O(n)', 'O(1)', 'linear_scan'))
    # C++ O(n log n) sort
    out.append(rec(r'''void sortv(std::vector<int>& a){ std::sort(a.begin(), a.end()); }''', 'cpp', 'O(n log n)', 'O(1)', 'sort'))
    # C++ O(n^2) bubble
    out.append(rec(r'''void bubble(int* a,int n){ for(int i=0;i<n-1;i++){ for(int j=0;j<n-i-1;j++){ if(a[j]>a[j+1]){int t=a[j];a[j]=a[j+1];a[j+1]=t;} } } }''', 'cpp', 'O(n²)', 'O(1)', 'bubble'))
    # C++ O(n^3) MCM DP
    out.append(rec(r'''int mco(int p[], int n){ int m[n][n]; for(int i=1;i<n;i++) m[i][i]=0; for(int L=2;L<n;L++){ for(int i=1;i<n-L+1;i++){ int j=i+L-1; m[i][j]=1e9; for(int k=i;k<=j-1;k++){ int q=m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j]; if(q<m[i][j]) m[i][j]=q; } } } return m[1][n-1]; }''', 'cpp', 'O(n³)', 'O(n²)', 'dp'))
    # C++ O(2^n) subsets
    out.append(rec(r'''int cnt=0; void gen(std::vector<int>& a,int i){ if(i==(int)a.size()){cnt++;return;} gen(a,i+1); gen(a,i+1);}''', 'cpp', 'O(2ⁿ)', 'O(n)', 'backtracking'))
    # C++ O(n!) permutations
    out.append(rec(r'''void perm(std::vector<int>& a,int l){ if(l==(int)a.size()) return; for(int i=l;i<(int)a.size();i++){ std::swap(a[l],a[i]); perm(a,l+1); std::swap(a[l],a[i]); } }''', 'cpp', 'O(n!)', 'O(n)', 'permutations'))

    # Java O(1)
    out.append(rec(r'''class C{int f(int[] a){return a[0];}}''', 'java', 'O(1)', 'O(1)', 'constant'))
    # Java O(log n)
    out.append(rec(r'''class C{int bs(int[] a,int x){int l=0,r=a.length-1;while(l<=r){int mid=l+(r-l)/2; if(a[mid]==x)return mid; if(a[mid]<x) l=mid+1; else r=mid-1;}return -1;}}''', 'java', 'O(log n)', 'O(1)', 'binary_search'))
    # Java O(n)
    out.append(rec(r'''class C{int sum(int[] a){int s=0; for(int x: a) s+=x; return s;}}''', 'java', 'O(n)', 'O(1)', 'linear_scan'))
    # Java O(n log n) sort
    out.append(rec(r'''import java.util.*; class C{void s(int[] a){ Arrays.sort(a); }}''', 'java', 'O(n log n)', 'O(1)', 'sort'))
    # Java O(n^2) bubble
    out.append(rec(r'''class C{void b(int[] a){int n=a.length; for(int i=0;i<n-1;i++){ for(int j=0;j<n-i-1;j++){ if(a[j]>a[j+1]){int t=a[j];a[j]=a[j+1];a[j+1]=t;} } } }}''', 'java', 'O(n²)', 'O(1)', 'bubble'))
    # Java O(n^3) triple loop
    out.append(rec(r'''class C{int f(int n){int s=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) for(int k=0;k<n;k++) s++; return s;}}''', 'java', 'O(n³)', 'O(1)', 'triple_loop'))
    # Java O(2^n)
    out.append(rec(r'''class C{int c=0; void g(int[] a,int i){ if(i==a.length){c++;return;} g(a,i+1); g(a,i+1);} }''', 'java', 'O(2ⁿ)', 'O(n)', 'backtracking'))
    # Java O(n!)
    out.append(rec(r'''class C{ void p(int[] a,int l){ if(l==a.length)return; for(int i=l;i<a.length;i++){ int t=a[l];a[l]=a[i];a[i]=t; p(a,l+1); t=a[l];a[l]=a[i];a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # Extra targeted variants to strengthen weak classes
    # C++ Merge Sort variant with vectors
    out.append(rec(r'''void merge(std::vector<int>& a,int l,int m,int r){int n1=m-l+1,n2=r-m; std::vector<int> L(n1),R(n2); for(int i=0;i<n1;i++)L[i]=a[l+i]; for(int j=0;j<n2;j++)R[j]=a[m+1+j]; int i=0,j=0,k=l; while(i<n1 && j<n2) a[k++]=(L[i]<=R[j]?L[i++]:R[j++]); while(i<n1)a[k++]=L[i++]; while(j<n2)a[k++]=R[j++];}
void ms(std::vector<int>& a,int l,int r){ if(l<r){ int m=l+(r-l)/2; ms(a,l,m); ms(a,m+1,r); merge(a,l,m,r);} }''', 'cpp', 'O(n log n)', 'O(n)', 'merge_sort'))
    # C++ Merge Sort variant using arrays
    out.append(rec(r'''void merge(int a[],int l,int m,int r){ int n1=m-l+1,n2=r-m; int L[n1],R[n2]; for(int i=0;i<n1;i++)L[i]=a[l+i]; for(int j=0;j<n2;j++)R[j]=a[m+1+j]; int i=0,j=0,k=l; while(i<n1 && j<n2) a[k++]=(L[i]<=R[j]?L[i++]:R[j++]); while(i<n1)a[k++]=L[i++]; while(j<n2)a[k++]=R[j++]; }
void ms(int a[],int l,int r){ if(l<r){ int m=l+(r-l)/2; ms(a,l,m); ms(a,m+1,r); merge(a,l,m,r);} }''', 'cpp', 'O(n log n)', 'O(n)', 'merge_sort'))
    # Java Merge Sort variant
    out.append(rec(r'''class C{ void merge(int[] a,int l,int m,int r){ int n1=m-l+1,n2=r-m; int[] L=new int[n1],R=new int[n2]; for(int i=0;i<n1;i++)L[i]=a[l+i]; for(int j=0;j<n2;j++)R[j]=a[m+1+j]; int i=0,j=0,k=l; while(i<n1 && j<n2) a[k++]=(L[i]<=R[j]?L[i++]:R[j++]); while(i<n1)a[k++]=L[i++]; while(j<n2)a[k++]=R[j++]; }
 void ms(int[] a,int l,int r){ if(l<r){ int m=l+(r-l)/2; ms(a,l,m); ms(a,m+1,r); merge(a,l,m,r);} }}''', 'java', 'O(n log n)', 'O(n)', 'merge_sort'))

    # Permutations variants
    out.append(rec(r'''void perm(std::vector<int>& a,int l){ if(l==(int)a.size()) return; for(int i=l;i<(int)a.size();i++){ std::iter_swap(a.begin()+l,a.begin()+i); perm(a,l+1); std::iter_swap(a.begin()+l,a.begin()+i);} }''', 'cpp', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class C{ void p(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ int t=a[l]; a[l]=a[i]; a[i]=t; p(a,l+1); t=a[l]; a[l]=a[i]; a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # TreeMap loop variants
    out.append(rec(r'''import java.util.*; class C{ void f(List<Integer> a){ TreeMap<Integer,Integer> t=new TreeMap<>(); for(int x: a){ t.put(x, t.getOrDefault(x,0)+1); } } }''', 'java', 'O(n log n)', 'O(n)', 'balanced_tree'))
    out.append(rec(r'''import java.util.*; class C{ void f(int[] a){ TreeMap<Integer,Integer> t=new TreeMap<>(); for(int i=0;i<a.length;i++){ t.put(a[i], t.getOrDefault(a[i],0)+1); } } }''', 'java', 'O(n log n)', 'O(n)', 'balanced_tree'))

    # Additional balanced variants
    # Binary search variants
    out.append(rec(r'''int bs2(std::vector<int>& a,int x){int l=0,r=(int)a.size()-1;while(l<=r){int m=(l+r)/2; if(a[m]==x) return m; if(a[m]<x) l=m+1; else r=m-1;} return -1;}''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''class B{int bs2(int[] a,int x){int l=0,r=a.length-1;while(l<=r){int m=(l+r)/2; if(a[m]==x) return m; if(a[m]<x) l=m+1; else r=m-1;} return -1;}}''', 'java', 'O(log n)', 'O(1)', 'binary_search'))

    # Bubble sort slight variations
    out.append(rec(r'''void bub2(std::vector<int>& a){int n=a.size(); for(int i=0;i<n;i++){ for(int j=1;j<n-i;j++){ if(a[j]<a[j-1]) std::swap(a[j],a[j-1]); } } }''', 'cpp', 'O(n²)', 'O(1)', 'bubble'))
    out.append(rec(r'''class B{ void b2(int[] a){int n=a.length; for(int i=0;i<n;i++){ for(int j=1;j<n-i;j++){ if(a[j]<a[j-1]){ int t=a[j]; a[j]=a[j-1]; a[j-1]=t; } } } } }''', 'java', 'O(n²)', 'O(1)', 'bubble'))

    # Triple nested loops (n^3)
    out.append(rec(r'''int tri(std::vector<int>& a){int n=a.size(), s=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) for(int k=0;k<n;k++) s+=a[(i+j+k)%n]; return s;}''', 'cpp', 'O(n³)', 'O(1)', 'triple_loop'))
    out.append(rec(r'''class T{ int tri(int n){int s=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) for(int k=0;k<n;k++) s++; return s; } }''', 'java', 'O(n³)', 'O(1)', 'triple_loop'))

    # Exponential (2^n) subsets/backtracking variants
    out.append(rec(r'''int cnt2=0; void gen2(std::vector<int>& a,int i){ if(i==(int)a.size()){cnt2++;return;} gen2(a,i+1); gen2(a,i+1);}''', 'cpp', 'O(2ⁿ)', 'O(n)', 'backtracking'))
    out.append(rec(r'''class E{ int c=0; void g(int[] a,int i){ if(i==a.length){c++;return;} g(a,i+1); g(a,i+1);} }''', 'java', 'O(2ⁿ)', 'O(n)', 'backtracking'))

    # TreeMap loops more variants
    out.append(rec(r'''import java.util.*; class Tm{ void f(List<Integer> a){ TreeMap<Integer,Integer> t=new TreeMap<>(); for(Integer x: a){ t.put(x, t.getOrDefault(x,0)+1); } } }''', 'java', 'O(n log n)', 'O(n)', 'balanced_tree'))
    out.append(rec(r'''import java.util.*; class Tm2{ void f(Set<Integer> a){ TreeMap<Integer,Integer> t=new TreeMap<>(); for(Integer x: a){ t.put(x, 1); } } }''', 'java', 'O(n log n)', 'O(n)', 'balanced_tree'))

    # Sorting (n log n) variants
    out.append(rec(r'''void s2(std::vector<int>& a){ std::stable_sort(a.begin(), a.end()); }''', 'cpp', 'O(n log n)', 'O(1)', 'sort'))
    out.append(rec(r'''class S{ void s2(int[] a){ java.util.Arrays.sort(a); } }''', 'java', 'O(n log n)', 'O(1)', 'sort'))

    # Factorial (n!) more variants
    out.append(rec(r'''void perm2(std::vector<int>& a){ do { /* visit */ } while(std::next_permutation(a.begin(), a.end())); }''', 'cpp', 'O(n!)', 'O(1)', 'permutations'))
    out.append(rec(r'''class P{ void p2(int[] a,int l){ if(l==a.length)return; for(int i=l;i<a.length;i++){ int t=a[l];a[l]=a[i];a[i]=t; p2(a,l+1); t=a[l];a[l]=a[i];a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # More O(n^3) DP-like and triple loops
    out.append(rec(r'''int dp3(int n){ std::vector<std::vector<int>> m(n, std::vector<int>(n,0)); for(int L=2;L<n;L++){ for(int i=1;i<n-L+1;i++){ int j=i+L-1; m[i][j]=1e9; for(int k=i;k<j;k++){ m[i][j]=std::min(m[i][j], m[i][k]+m[k+1][j]+i*k*j); } } } return m[1][n-1]; }''', 'cpp', 'O(n³)', 'O(n²)', 'dp'))
    out.append(rec(r'''class D{ int mco(int[] p){ int n=p.length; int[][] m=new int[n][n]; for(int L=2;L<n;L++){ for(int i=1;i<n-L+1;i++){ int j=i+L-1; m[i][j]=Integer.MAX_VALUE; for(int k=i;k<j;k++){ m[i][j]=Math.min(m[i][j], m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j]); } } } return m[1][n-1]; } }''', 'java', 'O(n³)', 'O(n²)', 'dp'))
    out.append(rec(r'''int triple2(int n){ int s=0; for(int i=0;i<n;i++){ for(int j=0;j<=i;j++){ for(int k=0;k<j;k++){ s+=i+j+k; } } } return s; }''', 'cpp', 'O(n³)', 'O(1)', 'triple_loop'))
    out.append(rec(r'''class T2{ int tri2(int n){ int s=0; for(int i=0;i<n;i++){ for(int j=0;j<=i;j++){ for(int k=0;k<j;k++){ s++; } } } return s; } }''', 'java', 'O(n³)', 'O(1)', 'triple_loop'))

    # More O(n!) permutations
    out.append(rec(r'''void perm3(std::vector<int>& a,int l){ if(l==(int)a.size()) return; for(int i=l;i<(int)a.size();i++){ int t=a[l]; a[l]=a[i]; a[i]=t; perm3(a,l+1); a[i]=a[l]; a[l]=t; } }''', 'cpp', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class P3{ void p3(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ int t=a[l]; a[l]=a[i]; a[i]=t; p3(a,l+1); t=a[l]; a[l]=a[i]; a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # Focused MCM DP (O(n^3)) more patterns
    out.append(rec(r'''int mco2(std::vector<int>& p){int n=p.size(); std::vector<std::vector<int>> m(n, std::vector<int>(n,0)); for(int L=2;L<n;L++){ for(int i=1;i<n-L+1;i++){ int j=i+L-1; m[i][j]=INT_MAX; for(int k=i;k<j;k++){ m[i][j]=std::min(m[i][j], m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j]); } } } return m[1][n-1]; }''', 'cpp', 'O(n³)', 'O(n²)', 'dp'))
    out.append(rec(r'''class D2{ int mco2(int[] p){int n=p.length; int[][] m=new int[n][n]; for(int L=2;L<n;L++){ for(int i=1;i<n-L+1;i++){ int j=i+L-1; m[i][j]=Integer.MAX_VALUE; for(int k=i;k<j;k++){ m[i][j]=Math.min(m[i][j], m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j]); } } } return m[1][n-1]; } }''', 'java', 'O(n³)', 'O(n²)', 'dp'))

    # More permutations (O(n!))
    out.append(rec(r'''void perm4(std::vector<int>& a,int l){ if(l==(int)a.size()) return; for(int i=l;i<(int)a.size();++i){ std::swap(a[l],a[i]); perm4(a,l+1); std::swap(a[l],a[i]); } }''', 'cpp', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class P4{ void p4(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ int t=a[l]; a[l]=a[i]; a[i]=t; p4(a,l+1); t=a[l]; a[l]=a[i]; a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # More binary search (O(log n)) idioms
    out.append(rec(r'''int lb(std::vector<int>& a,int x){int l=0,r=a.size(); while(l<r){ int m=l+(r-l)/2; if(a[m]<x) l=m+1; else r=m; } return l; }''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''class B3{ int lb(int[] a,int x){int l=0,r=a.length; while(l<r){ int m=l+(r-l)/2; if(a[m]<x) l=m+1; else r=m; } return l; } }''', 'java', 'O(log n)', 'O(1)', 'binary_search'))

    # Hard negatives: linear scans that look like while loops (not binary search)
    out.append(rec(r'''int scan(std::vector<int>& a,int x){int i=0; while(i<(int)a.size()){ if(a[i]==x) return i; i++; } return -1;}''', 'cpp', 'O(n)', 'O(1)', 'linear_scan'))
    out.append(rec(r'''class HN1{ int scan(int[] a,int x){int i=0; while(i<a.length){ if(a[i]==x) return i; i++; } return -1; } }''', 'java', 'O(n)', 'O(1)', 'linear_scan'))

    # Hard negatives: two-pointer loops (not binary search)
    out.append(rec(r'''int twop(std::vector<int>& a){int i=0,j=(int)a.size()-1, cnt=0; while(i<j){ if(a[i]+a[j]>0) j--; else i++; cnt++; } return cnt;}''', 'cpp', 'O(n)', 'O(1)', 'two_pointer'))
    out.append(rec(r'''class HN2{ int twop(int[] a){int i=0,j=a.length-1, cnt=0; while(i<j){ if(a[i]+a[j]>0) j--; else i++; cnt++; } return cnt; } }''', 'java', 'O(n)', 'O(1)', 'two_pointer'))

    # Hard negatives: nested loops permutations counter but not generating all permutations (O(n^2) or O(n^3))
    out.append(rec(r'''long pairs(std::vector<int>& a){ long c=0; int n=a.size(); for(int i=0;i<n;i++){ for(int j=i+1;j<n;j++){ if(a[i]<a[j]) c++; } } return c;}''', 'cpp', 'O(n²)', 'O(1)', 'nested_loops'))
    out.append(rec(r'''class HN3{ long pairs(int[] a){ long c=0; int n=a.length; for(int i=0;i<n;i++){ for(int j=i+1;j<n;j++){ if(a[i]<a[j]) c++; } } return c; } }''', 'java', 'O(n²)', 'O(1)', 'nested_loops'))

    # Hard negatives: triple loops without DP table (should remain O(n^3) but helps separator vs MCM DP)
    out.append(rec(r'''long tri3(int n){ long s=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) for(int k=0;k<n;k++) s+=i+j+k; return s;}''', 'cpp', 'O(n³)', 'O(1)', 'triple_loop'))
    out.append(rec(r'''class HN4{ long tri3(int n){ long s=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) for(int k=0;k<n;k++) s++; return s; } }''', 'java', 'O(n³)', 'O(1)', 'triple_loop'))

    # Hard negatives: factorial-like loops that are actually O(n^2)
    out.append(rec(r'''long factLike(int n){ long s=0; for(int i=0;i<n;i++){ for(int j=0;j<=i;j++){ s+=i*j; } } return s;}''', 'cpp', 'O(n²)', 'O(1)', 'nested_loops'))
    out.append(rec(r'''class HN5{ long f(int n){ long s=0; for(int i=0;i<n;i++){ for(int j=0;j<=i;j++){ s+=i*j; } } return s; } }''', 'java', 'O(n²)', 'O(1)', 'nested_loops'))

    # More binary search idioms (guard against misclassification)
    out.append(rec(r'''int ub(std::vector<int>& a,int x){int l=0,r=a.size(); while(l<r){ int m=(l+r)/2; if(a[m]<=x) l=m+1; else r=m; } return l; }''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''int idx(std::vector<int>& a,int x){int l=0,r=(int)a.size()-1; while(l<=r){ int m=(l+r)>>1; if(a[m]==x) return m; if(a[m]<x) l=m+1; else r=m-1; } return -1; }''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''class B4{ int ub(int[] a,int x){int l=0,r=a.length; while(l<r){ int m=(l+r)>>>1; if(a[m]<=x) l=m+1; else r=m; } return l; } }''', 'java', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''class B5{ int idx(int[] a,int x){int l=0,r=a.length-1; while(l<=r){ int m=(l+r)>>>1; if(a[m]==x) return m; if(a[m]<x) l=m+1; else r=m-1; } return -1; } }''', 'java', 'O(log n)', 'O(1)', 'binary_search'))

    # More Java permutations forms
    out.append(rec(r'''class PJ1{ void p(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ swap(a,l,i); p(a,l+1); swap(a,l,i);} } void swap(int[] a,int i,int j){ int t=a[i]; a[i]=a[j]; a[j]=t; } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class PJ2{ void p(int[] a){ perm(a,0);} void perm(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ int t=a[l];a[l]=a[i];a[i]=t; perm(a,l+1); t=a[l];a[l]=a[i];a[i]=t; } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class PJ3{ void p(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ if(i!=l){ int t=a[l];a[l]=a[i];a[i]=t; } p(a,l+1); if(i!=l){ int t=a[l];a[l]=a[i];a[i]=t; } } } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    # Final targeted additions
    # Binary search canonical minimal forms
    out.append(rec(r'''int bs_min(std::vector<int>& a,int x){int l=0,r=(int)a.size()-1;while(l<=r){int m=(l+r)/2; if(a[m]==x)return m; if(a[m]<x) l=m+1; else r=m-1;} return -1;}''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))
    out.append(rec(r'''class Bmin{ int bs_min(int[] a,int x){int l=0,r=a.length-1;while(l<=r){int m=(l+r)>>>1; if(a[m]==x)return m; if(a[m]<x) l=m+1; else r=m-1;} return -1;} }''', 'java', 'O(log n)', 'O(1)', 'binary_search'))

    # Binary search with long indices
    out.append(rec(r'''long bs_long(std::vector<long>& a,long x){long l=0,r=(long)a.size()-1; while(l<=r){ long m=l+((r-l)>>1); if(a[m]==x) return m; if(a[m]<x) l=m+1; else r=m-1;} return -1;}''', 'cpp', 'O(log n)', 'O(1)', 'binary_search'))

    # Java permutations with helper swap and separate method
    out.append(rec(r'''class PJ4{ void solve(int[] a){ perm(a,0);} void perm(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ swap(a,l,i); perm(a,l+1); swap(a,l,i);} } void swap(int[] a,int i,int j){ int t=a[i]; a[i]=a[j]; a[j]=t; } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))
    out.append(rec(r'''class PJ5{ void perm(int[] a,int l){ if(l==a.length) return; for(int i=l;i<a.length;i++){ if(i!=l) swap(a,l,i); perm(a,l+1); if(i!=l) swap(a,l,i);} } void swap(int[] a,int i,int j){ int t=a[i]; a[i]=a[j]; a[j]=t; } }''', 'java', 'O(n!)', 'O(n)', 'permutations'))

    return out


def main():
    with open(DATASET_PATH, 'r') as f:
        data = json.load(f)
    orig = len(data)
    data.extend(samples())
    with open(DATASET_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Added {len(data)-orig} samples. Total: {len(data)}")


if __name__ == '__main__':
    main()
