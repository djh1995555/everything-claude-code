---
name: cpp-coding-standards
description: 基于C++核心指南（isocpp.github.io）的C++编码标准。在编写、审查或重构C++代码时使用，以实施现代、安全和惯用的实践。
origin: ECC
---

# C++编码标准（C++核心指南）

现代C++（C++17/20/23）的综合编码标准，源自[C++核心指南](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)。实施类型安全、资源安全、不可变性和清晰度。

## 使用时机

- 编写新的C++代码（类、函数、模板）
- 审查或重构现有的C++代码
- 在C++项目中做出架构决策
- 在C++代码库中实施一致的风格
- 在语言特性之间进行选择（例如，`enum` vs `enum class`，原始指针 vs 智能指针）

### 不使用时机

- 非C++项目
- 无法采用现代C++特性的遗留C代码库
- 嵌入式/裸机上下文，其中特定指南与硬件约束冲突（选择性调整）

## 跨领域原则

这些主题贯穿整个指南，构成基础：

1. **RAII无处不在**（P.8, R.1, E.6, CP.20）：将资源生命周期绑定到对象生命周期
2. **默认不可变**（P.10, Con.1-5, ES.25）：从`const`/`constexpr`开始；可变性是例外
3. **类型安全**（P.4, I.4, ES.46-49, Enum.3）：使用类型系统在编译时防止错误
4. **表达意图**（P.3, F.1, NL.1-2, T.10）：名称、类型和概念应传达目的
5. **最小化复杂性**（F.2-3, ES.5, Per.4-5）：简单的代码是正确的代码
6. **值语义优于指针语义**（C.10, R.3-5, F.20, CP.31）：优先按值返回和作用域对象

## 哲学与接口（P.*, I.*）

### 关键规则

| 规则 | 摘要 |
|------|---------|
| **P.1** | 直接在代码中表达想法 |
| **P.3** | 表达意图 |
| **P.4** | 理想情况下，程序应该是静态类型安全的 |
| **P.5** | 优先编译时检查而非运行时检查 |
| **P.8** | 不泄漏任何资源 |
| **P.10** | 优先不可变数据而非可变数据 |
| **I.1** | 使接口显式 |
| **I.2** | 避免非const全局变量 |
| **I.4** | 使接口精确且强类型 |
| **I.11** | 永远不要通过原始指针或引用转移所有权 |
| **I.23** | 保持函数参数数量少 |

### 推荐

```cpp
// P.10 + I.4: 不可变、强类型接口
struct Temperature {
    double kelvin;
};

Temperature boil(const Temperature& water);
```

### 不推荐

```cpp
// 弱接口：所有权不明确，单位不明确
double boil(double* temp);

// 非const全局变量
int g_counter = 0;  // 违反I.2
```

## 函数（F.*）

### 关键规则

| 规则 | 摘要 |
|------|---------|
| **F.1** | 将有意义的操作打包为精心命名的函数 |
| **F.2** | 函数应执行单一逻辑操作 |
| **F.3** | 保持函数简短和简单 |
| **F.4** | 如果函数可能在编译时求值，声明为`constexpr` |
| **F.6** | 如果函数必须不抛出，声明为`noexcept` |
| **F.8** | 优先纯函数 |
| **F.16** | 对于"输入"参数，通过值传递廉价复制的类型，其他通过`const&` |
| **F.20** | 对于"输出"值，优先返回值而非输出参数 |
| **F.21** | 要返回多个"输出"值，优先返回结构体 |
| **F.43** | 永远不要返回指向局部对象的指针或引用 |

### 参数传递

```cpp
// F.16: 廉价类型通过值，其他通过const&
void print(int x);                           // 廉价：通过值
void analyze(const std::string& data);       // 昂贵：通过const&
void transform(std::string s);               // 接收器：通过值（将移动）

// F.20 + F.21: 返回值，而非输出参数
struct ParseResult {
    std::string token;
    int position;
};

ParseResult parse(std::string_view input);   // 推荐：返回结构体

// 不推荐：输出参数
void parse(std::string_view input,
           std::string& token, int& pos);    // 避免这样
```

### 纯函数和constexpr

```cpp
// F.4 + F.8: 纯函数，尽可能constexpr
constexpr int factorial(int n) noexcept {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

static_assert(factorial(5) == 120);
```

### 反模式

- 从函数返回`T&&`（F.45）
- 使用`va_arg` / C风格可变参数（F.55）
- 在传递给其他线程的lambda中按引用捕获（F.53）
- 返回`const T`，这会抑制移动语义（F.49）

## 类与类层次结构（C.*）

### 关键规则

| 规则 | 摘要 |
|------|---------|
| **C.2** | 如果存在不变量，使用`class`；如果数据成员独立变化，使用`struct` |
| **C.9** | 最小化成员的暴露 |
| **C.20** | 如果可以避免定义默认操作，就避免（零规则） |
| **C.21** | 如果定义或`=delete`任何复制/移动/析构函数，处理所有这些（五规则） |
| **C.35** | 基类析构函数：public virtual或protected non-virtual |
| **C.41** | 构造函数应创建完全初始化的对象 |
| **C.46** | 声明单参数构造函数为`explicit` |
| **C.67** | 多态类应抑制public复制/移动 |
| **C.128** | 虚函数：精确指定`virtual`、`override`或`final`中的一个 |

### 零规则

```cpp
// C.20: 让编译器生成特殊成员
struct Employee {
    std::string name;
    std::string department;
    int id;
    // 不需要析构函数、复制/移动构造函数或赋值运算符
};
```

### 五规则

```cpp
// C.21: 如果必须管理资源，定义所有五个
class Buffer {
public:
    explicit Buffer(std::size_t size)
        : data_(std::make_unique<char[]>(size)), size_(size) {}

    ~Buffer() = default;

    Buffer(const Buffer& other)
        : data_(std::make_unique<char[]>(other.size_)), size_(other.size_) {
        std::copy_n(other.data_.get(), size_, data_.get());
    }

    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            auto new_data = std::make_unique<char[]>(other.size_);
            std::copy_n(other.data_.get(), other.size_, new_data.get());
            data_ = std::move(new_data);
            size_ = other.size_;
        }
        return *this;
    }

    Buffer(Buffer&&) noexcept = default;
    Buffer& operator=(Buffer&&) noexcept = default;

private:
    std::unique_ptr<char[]> data_;
    std::size_t size_;
};
```

### 类层次结构

```cpp
// C.35 + C.128: 虚析构函数，使用override
class Shape {
public:
    virtual ~Shape() = default;