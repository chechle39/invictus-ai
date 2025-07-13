Next version:

- Web interface: Upload file project/Drag & drop interface/Real-time progress/Download results
- Base on user requirements to suggest proper language/technology

# 🚀 AI Migration Map Generator

**AI-powered tool for analyzing legacy systems and generating migration maps**

## 📋 Tóm tắt

AI Migration Map Generator hỗ trợ **2 chế độ chính**:

### 🎯 **Chế độ 1: Tự động đề xuất công nghệ**

- AI phân tích hệ thống và **tự động gợi ý** công nghệ phù hợp nhất
- Dựa trên: mục đích sử dụng, performance, team expertise, budget
- **Command**: `ai-migration-map suggest`

### 🎯 **Chế độ 2: Chuyển đổi theo yêu cầu**

- User chỉ định **công nghệ mong muốn** để migrate sang
- Hỗ trợ: framework upgrades, language migrations, architecture changes
- **Command**: `ai-migration-map generate`

## 🚀 Hướng dẫn sử dụng

### Cài đặt

```bash
python --version  # Python 3.8+
export OPENAI_API_KEY="your-api-key-here"
pip install -r requirements.txt
pip install -e .
```

### Sử dụng cơ bản

```bash
# 1. Phân tích hệ thống legacy
ai-migration-map analyze ./legacy-project -o analysis.json

# 2A. Chế độ tự động đề xuất công nghệ
ai-migration-map suggest analysis.json --use-case web-app --performance-requirement high

# 2B. Chế độ chuyển đổi theo yêu cầu
ai-migration-map generate analysis.json -t dotnet-6
```

### Chế độ 1: Tự động đề xuất công nghệ

```bash
# Gợi ý cho web app performance cao
ai-migration-map suggest analysis.json --use-case web-app --performance-requirement high

# Gợi ý cho startup budget thấp
ai-migration-map suggest analysis.json --use-case startup --budget-constraint low --team-expertise javascript

# Gợi ý cho enterprise
ai-migration-map suggest analysis.json --use-case enterprise --performance-requirement high --team-expertise java
```

### Chế độ 2: Chuyển đổi theo yêu cầu

```bash
# Framework upgrades
ai-migration-map generate analysis.json -t dotnet-6
ai-migration-map generate analysis.json -t java-spring-boot

# Language migrations
ai-migration-map generate analysis.json -t java-spring-boot --source-language csharp --target-language java
ai-migration-map generate analysis.json -t node-express --source-language python --target-language javascript

# Architecture changes
ai-migration-map generate analysis.json -t microservices
ai-migration-map generate analysis.json -t cloud-native
```

## 🎯 Hỗ trợ

### Use Cases

- **web-app**: Web applications
- **api-service**: API services
- **microservices**: Microservices architecture
- **enterprise**: Enterprise applications
- **startup**: Startup applications

### Technology Stacks

- **dotnet-6**: .NET Framework → .NET 6
- **java-spring-boot**: Java 8 → Spring Boot 3
- **node-express**: Legacy → Node.js Express
- **go-microservices**: Java/C# → Go Microservices
- **rust-web**: C#/Java → Rust Web
- **microservices**: Monolith → Microservices
- **cloud-native**: On-premise → Cloud-native

### Programming Languages

- **C# → Java**: Enterprise applications
- **Python → JavaScript**: Web applications
- **Java → Go**: Performance-critical services
- **PHP → Python**: Legacy web apps

## 📊 Output mẫu

### Migration Map (JSON)

```json
{
  "project": "LegacyECommerce",
  "source_stack": ".NET Framework 4.7",
  "target_stack": ".NET 6 Microservices",
  "migration_strategy": {
    "direct_conversion": ["Models/Product.cs"],
    "rewrite_required": ["Controllers/ProductController.cs"],
    "special_handling": ["LegacyAuthenticationMiddleware.cs"]
  },
  "technology_mapping": {
    "System.Web.Http": "Microsoft.AspNetCore.Mvc",
    "Entity Framework 6": "Entity Framework Core"
  },
  "estimated_effort": "3-4 weeks"
}
```

### Technology Suggestions

```
🏆 Primary Recommendations:
  1. java-spring-boot
  2. dotnet-6
  3. go-microservices

✅ Pros & Cons:
  java-spring-boot:
    ✅ Pros: Mature ecosystem, Excellent enterprise features
    ❌ Cons: Verbose syntax, Higher memory usage
```

## 🔧 Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-4"
```

### API Key Usage

API key được sử dụng để:

- **Phân tích hệ thống** bằng AI
- **Gợi ý công nghệ** phù hợp
- **Tạo migration maps** thông minh
- **Validate** migration plans

**AI Migration Map Generator - Công cụ AI mạnh mẽ để tự động hóa việc migration hệ thống legacy!** 🚀
