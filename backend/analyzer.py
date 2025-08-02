import ast
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import os

@dataclass
class ComplexityPattern:
    pattern: str
    time_complexity: str
    space_complexity: str
    description: str
    confidence: float

class TimeComplexityAnalyzer:
    def __init__(self):
        self.python_patterns = self._init_python_patterns()
        self.cpp_patterns = self._init_cpp_patterns()
        self.java_patterns = self._init_java_patterns()
        self.javascript_patterns = self._init_javascript_patterns()
    
    def _init_tree_sitter(self):
        """Initialize tree-sitter parsers for different languages"""
        # Tree-sitter is not available, using regex-based analysis only
        pass
    
    def _init_python_patterns(self) -> List[ComplexityPattern]:
        """Initialize Python-specific complexity patterns"""
        return [
            ComplexityPattern(
                pattern=r"for\s+\w+\s+in\s+range\s*\(\s*\w+\s*\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Single loop with range",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"for\s+\w+\s+in\s+\w+",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Single loop over iterable",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"for\s+\w+\s+in\s+range\s*\(\s*\w+\s*\):\s*\n\s*for\s+\w+\s+in\s+range\s*\(\s*\w+\s*\)",
                time_complexity="O(n²)",
                space_complexity="O(1)",
                description="Nested loops",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"def\s+\w+\s*\([^)]*\):\s*\n\s*return\s+\w+\s*\(\s*\w+\s*-\s*1\s*\)\s*\+\s*\w+\s*\(\s*\w+\s*-\s*2\s*\)",
                time_complexity="O(2ⁿ)",
                space_complexity="O(n)",
                description="Fibonacci-like recursion",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"\.sort\s*\(\s*\)",
                time_complexity="O(n log n)",
                space_complexity="O(1)",
                description="Built-in sort",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"while\s+left\s*<=\s*right",
                time_complexity="O(log n)",
                space_complexity="O(1)",
                description="Binary search pattern",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"mid\s*=\s*\(left\s*\+\s*right\)\s*//\s*2",
                time_complexity="O(log n)",
                space_complexity="O(1)",
                description="Binary search midpoint calculation",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"\.append\s*\(\s*\w+\s*\)",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="List append",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"in\s+\w+",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Membership test in list",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"in\s+set\s*\(\s*\w+\s*\)",
                time_complexity="O(1)",
                space_complexity="O(n)",
                description="Membership test in set",
                confidence=0.9
            )
        ]
    
    def _init_cpp_patterns(self) -> List[ComplexityPattern]:
        """Initialize C++-specific complexity patterns"""
        return [
            ComplexityPattern(
                pattern=r"for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+\s*;\s*\w+\+\+\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Single for loop",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+\s*;\s*\w+\+\+\)\s*\{\s*for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+\s*;\s*\w+\+\+\)",
                time_complexity="O(n²)",
                space_complexity="O(1)",
                description="Nested for loops",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"while\s*\(\s*\w+\s*!=\s*nullptr\s*\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Linked list traversal",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"while\s*\(\s*\w+\s*!=\s*nullptr\s*\|\|\s*\w+\s*!=\s*nullptr\s*\|\|\s*\w+\s*>\s*0\s*\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Linked list traversal with carry",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"sort\s*\(\s*\w+\.begin\s*\(\s*\)\s*,\s*\w+\.end\s*\(\s*\)\s*\)",
                time_complexity="O(n log n)",
                space_complexity="O(1)",
                description="STL sort",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"vector\s*<\s*\w+\s*>\s+\w+",
                time_complexity="O(1)",
                space_complexity="O(n)",
                description="Vector declaration",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"ListNode\*\s+\w+",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="ListNode pointer declaration",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"new\s+ListNode",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="ListNode allocation",
                confidence=0.8
            ),
            ComplexityPattern(
                pattern=r"->\s*val",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="Linked list value access",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"->\s*next",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="Linked list next pointer access",
                confidence=0.9
            )
        ]
    
    def _init_java_patterns(self) -> List[ComplexityPattern]:
        """Initialize Java-specific complexity patterns"""
        return [
            ComplexityPattern(
                pattern=r"for\s*\(\s*\w+\s+\w+\s*:\s*\w+\s*\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Enhanced for loop",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+\.length\s*;\s*\w+\+\+\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Array iteration",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"Arrays\.sort\s*\(\s*\w+\s*\)",
                time_complexity="O(n log n)",
                space_complexity="O(1)",
                description="Arrays.sort",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"ArrayList\s*<\s*\w+\s*>\s+\w+",
                time_complexity="O(1)",
                space_complexity="O(n)",
                description="ArrayList declaration",
                confidence=0.8
            )
        ]
    
    def _init_javascript_patterns(self) -> List[ComplexityPattern]:
        """Initialize JavaScript-specific complexity patterns"""
        return [
            ComplexityPattern(
                pattern=r"for\s*\(\s*let\s+\w+\s*=\s*\d+\s*;\s*\w+\s*<\s*\w+\.length\s*;\s*\w+\+\+\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="Array iteration",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"for\s*\(\s*const\s+\w+\s+of\s+\w+\s*\)",
                time_complexity="O(n)",
                space_complexity="O(1)",
                description="For...of loop",
                confidence=0.9
            ),
            ComplexityPattern(
                pattern=r"\.sort\s*\(\s*\(\s*\w+\s*,\s*\w+\s*\)\s*=>",
                time_complexity="O(n log n)",
                space_complexity="O(1)",
                description="Array sort with comparator",
                confidence=0.95
            ),
            ComplexityPattern(
                pattern=r"\.push\s*\(\s*\w+\s*\)",
                time_complexity="O(1)",
                space_complexity="O(1)",
                description="Array push",
                confidence=0.9
            )
        ]
    
    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze the time and space complexity of the given code.
        
        Args:
            code: Source code to analyze
            language: Programming language ('python', 'cpp', 'java', 'javascript')
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Get language-specific patterns
            patterns = getattr(self, f"{language}_patterns", [])
            
            # Perform AST analysis
            ast_analysis = self._analyze_ast(code, language)
            
            # Perform regex pattern matching
            pattern_analysis = self._analyze_patterns(code, patterns)
            
            # Combine results
            result = self._combine_analysis(ast_analysis, pattern_analysis)
            
            # If result is still "Unknown", use fallback analysis
            if result["time_complexity"] == "Unknown":
                fallback_result = self._fallback_analysis(code, language)
                # Use fallback if it has better confidence or if original is unknown
                if fallback_result["confidence"] > result["confidence"]:
                    result = fallback_result
            
            # Generate suggestions
            suggestions = self._generate_suggestions(result, code, language)
            
            return {
                "time_complexity": result["time_complexity"],
                "space_complexity": result["space_complexity"],
                "breakdown": result["breakdown"],
                "suggestions": suggestions,
                "confidence": result["confidence"]
            }
            
        except Exception as e:
            # Fallback to basic analysis
            return self._fallback_analysis(code, language)
    
    def _analyze_ast(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code using Abstract Syntax Tree"""
        if language == "python":
            return self._analyze_python_ast(code)
        else:
            return self._analyze_regex_based(code, language)
    
    def _analyze_python_ast(self, code: str) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code)
            analyzer = PythonASTAnalyzer()
            analyzer.visit(tree)
            return analyzer.get_results()
        except:
            return {"time_complexity": "Unknown", "space_complexity": "Unknown", "breakdown": [], "confidence": 0.0}
    
    def _analyze_regex_based(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code using regex patterns for non-Python languages"""
        try:
            # Get language-specific patterns
            patterns = getattr(self, f"{language}_patterns", [])
            return self._analyze_patterns(code, patterns)
        except:
            return {"time_complexity": "Unknown", "space_complexity": "Unknown", "breakdown": [], "confidence": 0.0}
    
    def _analyze_patterns(self, code: str, patterns: List[ComplexityPattern]) -> Dict[str, Any]:
        """Analyze code using regex patterns"""
        results = []
        max_confidence = 0.0
        
        for pattern in patterns:
            matches = re.findall(pattern.pattern, code, re.MULTILINE | re.DOTALL)
            if matches:
                results.append({
                    "pattern": pattern,
                    "matches": len(matches),
                    "description": pattern.description
                })
                max_confidence = max(max_confidence, pattern.confidence)
        
        if not results:
            return {"time_complexity": "Unknown", "space_complexity": "Unknown", "breakdown": [], "confidence": 0.0}
        
        # Determine overall complexity based on patterns
        time_complexity = self._determine_time_complexity(results)
        space_complexity = self._determine_space_complexity(results)
        
        breakdown = [f"Found {r['matches']} instances of {r['description']}" for r in results]
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "breakdown": breakdown,
            "confidence": max_confidence
        }
    
    def _determine_time_complexity(self, results: List[Dict]) -> str:
        """Determine overall time complexity from pattern results"""
        complexities = []
        
        for result in results:
            pattern = result["pattern"]
            matches = result["matches"]
            
            if "O(2ⁿ)" in pattern.time_complexity:
                complexities.append("O(2ⁿ)")
            elif "O(n²)" in pattern.time_complexity:
                complexities.append("O(n²)")
            elif "O(n log n)" in pattern.time_complexity:
                complexities.append("O(n log n)")
            elif "O(log n)" in pattern.time_complexity:
                complexities.append("O(log n)")
            elif "O(n)" in pattern.time_complexity:
                complexities.append("O(n)")
            elif "O(1)" in pattern.time_complexity:
                complexities.append("O(1)")
        
        if not complexities:
            return "Unknown"
        
        # Return the highest complexity
        if "O(2ⁿ)" in complexities:
            return "O(2ⁿ)"
        elif "O(n²)" in complexities:
            return "O(n²)"
        elif "O(n log n)" in complexities:
            return "O(n log n)"
        elif "O(log n)" in complexities:
            return "O(log n)"
        elif "O(n)" in complexities:
            return "O(n)"
        else:
            return "O(1)"
    
    def _determine_space_complexity(self, results: List[Dict]) -> str:
        """Determine overall space complexity from pattern results"""
        max_space = "O(1)"
        
        for result in results:
            pattern = result["pattern"]
            if "O(n)" in pattern.space_complexity:
                max_space = "O(n)"
        
        return max_space
    
    def _combine_analysis(self, ast_result: Dict, pattern_result: Dict) -> Dict[str, Any]:
        """Combine AST and pattern analysis results"""
        # Prefer AST results if available and confident
        if ast_result["confidence"] > pattern_result["confidence"]:
            return ast_result
        else:
            return pattern_result
    
    def _generate_suggestions(self, result: Dict, code: str, language: str) -> List[str]:
        """Generate optimization suggestions based on analysis"""
        suggestions = []
        
        time_complexity = result["time_complexity"]
        confidence = result.get("confidence", 0.0)
        
        if "O(2ⁿ)" in time_complexity:
            suggestions.append("Consider using dynamic programming or memoization to reduce complexity from O(2ⁿ) to O(n)")
            suggestions.append("Look for overlapping subproblems that can be cached")
        
        if "O(n²)" in time_complexity:
            suggestions.append("Consider using a hash map/set for O(1) lookups instead of nested loops")
            suggestions.append("If sorting is acceptable, sort first and use binary search for O(n log n)")
        
        if "O(n log n)" in time_complexity:
            suggestions.append("This is already quite efficient. Consider if O(n) is possible with a single pass")
        
        if "O(log n)" in time_complexity:
            suggestions.append("This is very efficient! Consider if O(1) is possible with hash tables or precomputation")
        
        if "O(n)" in time_complexity:
            suggestions.append("Consider if O(log n) is possible with binary search or divide-and-conquer")
        
        if "O(1)" in time_complexity:
            suggestions.append("This is optimal time complexity. Focus on space optimization if needed")
        
        if "Unknown" in time_complexity or confidence < 0.5:
            suggestions.append("Unable to determine complexity. Consider adding comments to clarify algorithm logic")
            suggestions.append("Try simplifying the code structure for better analysis")
            suggestions.append("Check if the code contains complex nested structures or recursion")
        
        # Language-specific suggestions
        if language == "python":
            if "in " in code and "set(" not in code:
                suggestions.append("Consider converting list to set for O(1) membership testing")
            if ".append(" in code and "list comprehension" not in code:
                suggestions.append("Consider using list comprehension for better readability and performance")
            if "range(" in code and "len(" in code:
                suggestions.append("Consider using enumerate() for cleaner iteration with indices")
        
        elif language == "cpp":
            if "for(" in code and "vector" in code:
                suggestions.append("Consider using range-based for loops for cleaner syntax")
            if "sort(" in code:
                suggestions.append("Consider using std::sort for O(n log n) sorting")
        
        elif language == "java":
            if "for(" in code and "length" in code:
                suggestions.append("Consider using enhanced for loops for cleaner iteration")
            if "Arrays.sort" in code:
                suggestions.append("Consider using Collections.sort for objects")
        
        elif language == "javascript":
            if "for(" in code and "length" in code:
                suggestions.append("Consider using for...of or forEach for cleaner iteration")
            if ".sort(" in code:
                suggestions.append("Consider providing a comparator function for custom sorting")
        
        return suggestions
    
    def _fallback_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Fallback analysis when AST parsing fails"""
        # Basic heuristics with improved detection
        lines = code.split('\n')
        code_lower = code.lower()
        
        # Count various patterns
        for_count = code.count('for')
        while_count = code.count('while')
        def_count = code.count('def')
        return_count = code.count('return')
        if_count = code.count('if')
        
        # C++ specific patterns
        cpp_class_count = code.count('class ')
        cpp_public_count = code.count('public:')
        cpp_private_count = code.count('private:')
        cpp_pointer_count = code.count('*')
        cpp_arrow_count = code.count('->')
        cpp_nullptr_count = code.count('nullptr')
        cpp_new_count = code.count('new ')
        
        # Check for recursion patterns
        has_recursion = def_count > 0 and return_count > 0 and any(
            '(' in line and ')' in line and 'return' in line 
            for line in lines if 'return' in line
        )
        
        # Check for nested loops
        has_nested_loops = (for_count > 1 or while_count > 1) and any(
            line.strip().startswith(('for', 'while')) and 
            any('for' in prev_line or 'while' in prev_line 
                for prev_line in lines[:lines.index(line)])
            for line in lines if line.strip().startswith(('for', 'while'))
        )
        
        # Check for single loops
        has_loops = for_count > 0 or while_count > 0
        
        # Check for data structures
        has_arrays = any(word in code_lower for word in ['array', 'list', 'vector', '[]'])
        has_maps = any(word in code_lower for word in ['map', 'dict', 'hash', '{}'])
        has_sets = any(word in code_lower for word in ['set', 'hashset'])
        
        # Check for C++ specific patterns
        is_cpp = (cpp_class_count > 0 and cpp_public_count > 0) or \
                 (cpp_pointer_count > 0 and cpp_arrow_count > 0) or \
                 (cpp_nullptr_count > 0) or \
                 (cpp_new_count > 0)
        
        # Determine complexity based on patterns
        if has_recursion:
            time_complexity = "O(2ⁿ)"  # Conservative estimate
            space_complexity = "O(n)"
            breakdown = [f"Detected {def_count} recursive function calls"]
        elif has_nested_loops:
            time_complexity = "O(n²)"
            space_complexity = "O(1)"
            breakdown = [f"Detected {for_count + while_count} nested loops"]
        elif has_loops:
            time_complexity = "O(n)"
            space_complexity = "O(1)"
            breakdown = [f"Detected {for_count + while_count} loops"]
        elif has_arrays or has_maps or has_sets:
            time_complexity = "O(1)"
            space_complexity = "O(n)"
            breakdown = ["Detected data structures"]
        else:
            time_complexity = "O(1)"
            space_complexity = "O(1)"
            breakdown = ["No loops or data structures detected"]
        
        # Add more context to breakdown
        if for_count > 0:
            breakdown.append(f"Found {for_count} for loops")
        if while_count > 0:
            breakdown.append(f"Found {while_count} while loops")
        if def_count > 0:
            breakdown.append(f"Found {def_count} function definitions")
        
        # Add C++ specific context
        if is_cpp:
            if cpp_class_count > 0:
                breakdown.append(f"Found {cpp_class_count} C++ class definitions")
            if cpp_pointer_count > 0:
                breakdown.append(f"Found {cpp_pointer_count} pointer operations")
            if cpp_nullptr_count > 0:
                breakdown.append(f"Found {cpp_nullptr_count} nullptr checks")
            if cpp_new_count > 0:
                breakdown.append(f"Found {cpp_new_count} dynamic allocations")
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "breakdown": breakdown,
            "confidence": 0.4
        }


class PythonASTAnalyzer(ast.NodeVisitor):
    """AST analyzer for Python code"""
    
    def __init__(self):
        self.loops = 0
        self.nested_loops = 0
        self.recursive_calls = 0
        self.function_definitions = []
        self.current_function = None
        self.loop_depth = 0
    
    def visit_For(self, node):
        self.loops += 1
        self.loop_depth += 1
        if self.loop_depth > 1:
            self.nested_loops += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_While(self, node):
        self.loops += 1
        self.loop_depth += 1
        if self.loop_depth > 1:
            self.nested_loops += 1
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_FunctionDef(self, node):
        self.function_definitions.append(node.name)
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.function_definitions:
            self.recursive_calls += 1
        self.generic_visit(node)
    
    def get_results(self):
        if self.recursive_calls > 0:
            time_complexity = "O(2ⁿ)"
            space_complexity = "O(n)"
            breakdown = [f"Found {self.recursive_calls} recursive calls"]
        elif self.nested_loops > 0:
            time_complexity = "O(n²)"
            space_complexity = "O(1)"
            breakdown = [f"Found {self.nested_loops} nested loops"]
        elif self.loops > 0:
            time_complexity = "O(n)"
            space_complexity = "O(1)"
            breakdown = [f"Found {self.loops} loops"]
        else:
            time_complexity = "O(1)"
            space_complexity = "O(1)"
            breakdown = ["No loops or recursion detected"]
        
        confidence = min(0.9, 0.3 + (self.loops * 0.1) + (self.recursive_calls * 0.2))
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "breakdown": breakdown,
            "confidence": confidence
        }


 