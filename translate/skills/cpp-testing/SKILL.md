---
name: cpp-testing
description: 仅在编写/更新/修复C++测试、配置GoogleTest/CTest、诊断失败或不稳定的测试，或添加覆盖率/消毒剂时使用。
origin: ECC
---

# C++测试（代理技能）

针对现代C++（C++17/20）的代理聚焦测试工作流，使用GoogleTest/GoogleMock与CMake/CTest。

## 使用时机

- 编写新的C++测试或修复现有测试
- 为C++组件设计单元/集成测试覆盖率
- 添加测试覆盖率、CI门控或回归保护
- 配置CMake/CTest工作流以实现一致执行
- 调查测试失败或不稳定行为
- 启用消毒剂以进行内存/竞争诊断

### 不使用时机

- 实现新的产品功能而不修改测试
- 与测试覆盖率或失败无关的大规模重构
- 性能调优而无需验证测试回归
- 非C++项目或非测试任务

## 核心概念

- **TDD循环**：红→绿→重构（先测试，最小修复，然后清理）。
- **隔离**：优先依赖注入和假对象而非全局状态。
- **测试布局**：`tests/unit`、`tests/integration`、`tests/testdata`。
- **模拟与假对象**：模拟用于交互，假对象用于有状态行为。
- **CTest发现**：使用`gtest_discover_tests()`实现稳定的测试发现。
- **CI信号**：先运行子集，然后使用`--output-on-failure`运行完整套件。

## TDD工作流

遵循红→绿→重构循环：

1. **红**：编写一个失败的测试，捕获新行为
2. **绿**：实现最小更改以通过测试
3. **重构**：在测试保持绿色的同时清理代码

```cpp
// tests/add_test.cpp
#include <gtest/gtest.h>

int Add(int a, int b); // 由生产代码提供。

TEST(AddTest, AddsTwoNumbers) { // 红
  EXPECT_EQ(Add(2, 3), 5);
}

// src/add.cpp
int Add(int a, int b) { // 绿
  return a + b;
}

// 重构：测试通过后简化/重命名
```

## 代码示例

### 基本单元测试（gtest）

```cpp
// tests/calculator_test.cpp
#include <gtest/gtest.h>

int Add(int a, int b); // 由生产代码提供。

TEST(CalculatorTest, AddsTwoNumbers) {
    EXPECT_EQ(Add(2, 3), 5);
}
```

### 测试夹具（gtest）

```cpp
// tests/user_store_test.cpp
// 伪代码存根：用项目类型替换UserStore/User。
#include <gtest/gtest.h>
#include <memory>
#include <optional>
#include <string>

struct User { std::string name; };
class UserStore {
public:
    explicit UserStore(std::string /*path*/) {}
    void Seed(std::initializer_list<User> /*users*/) {}
    std::optional<User> Find(const std::string &/*name*/) { return User{"alice"}; }
};

class UserStoreTest : public ::testing::Test {
protected:
    void SetUp() override {
        store = std::make_unique<UserStore>":memory:");
        store->Seed({{"alice"}, {"bob"}});
    }

    std::unique_ptr<UserStore> store;
};

TEST_F(UserStoreTest, FindsExistingUser) {
    auto user = store->Find("alice");
    ASSERT_TRUE(user.has_value());
    EXPECT_EQ(user->name, "alice");
}
```

### 模拟（gmock）

```cpp
// tests/notifier_test.cpp
#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <string>

class Notifier {
public:
    virtual ~Notifier() = default;
    virtual void Send(const std::string &message) = 0;
};

class MockNotifier : public Notifier {
public:
    MOCK_METHOD(void, Send, (const std::string &message), (override));
};

class Service {
public:
    explicit Service(Notifier &notifier) : notifier_(notifier) {}
    void Publish(const std::string &message) { notifier_.Send(message); }

private:
    Notifier &notifier_;
};

TEST(ServiceTest, SendsNotifications) {
    MockNotifier notifier;
    Service service(notifier);

    EXPECT_CALL(notifier, Send("hello")).Times(1);
    service.Publish("hello");
}
```

### CMake/CTest快速入门

```cmake
# CMakeLists.txt（节选）
cmake_minimum_required(VERSION 3.20)
project(example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
# 优先使用项目锁定的版本。如果使用标签，请根据项目策略使用固定版本。
set(GTEST_VERSION v1.17.0) # 根据项目策略调整。
FetchContent_Declare(
  googletest
  # Google Test框架（官方仓库）
  URL https://github.com/google/googletest/archive/refs/tags/${GTEST_VERSION}.zip
)
FetchContent_MakeAvailable(googletest)

add_executable(example_tests
  tests/calculator_test.cpp
  src/calculator.cpp
)
target_link_libraries(example_tests GTest::gtest GTest::gmock GTest::gtest_main)

enable_testing()
include(GoogleTest)
gtest_discover_tests(example_tests)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
ctest --test-dir build --output-on-failure
```

## 运行测试

```bash
ctest --test-dir build --output-on-failure
ctest --test-dir build -R ClampTest
ctest --test-dir build -R "UserStoreTest.*" --output-on-failure
```

```bash
./build/example_tests --gtest_filter=ClampTest.*
./build/example_tests --gtest_filter=UserStoreTest.FindsExistingUser
```

## 调试失败