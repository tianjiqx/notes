
# google api design

## REST API

面向资源的 API 通常被构建为资源层次结构，其中每个节点是一个“简单资源”或“集合资源”。
- 一个集合包含相同类型的资源列表。 例如，一个用户拥有一组联系人。
    - 集合 ID /buckets
- 资源具有一些状态和零个或多个子资源。 每个子资源可以是一个简单资源或一个集合资源。
    - 资源 ID /bucket-id

面向资源的 API 的关键特性是，强调资源（数据模型）甚于资源上执行的方法（功能）。典型的面向资源的 API 使用少量方法公开大量资源。方法可以是标准方法或自定义方法。对于本指南，标准方法有：List、Get、Create、Update 和 Delete。


“资源”是被命名的实体，“资源名称”是它们的标识符。每个资源都必须具有自己唯一的资源名称。 
- 资源名称由资源自身的 ID、任何父资源的 ID 及其 API 服务名称组成。


Gmail API
Gmail API 服务实现了 Gmail API 并公开了大多数 Gmail 功能。它具有以下资源模型：

```
API 服务：gmail.googleapis.com
用户集合：users/*。每个用户都拥有以下资源。
消息集合：users/*/messages/*。
线程集合：users/*/threads/*。
标签集合：users/*/labels/*。
变更历史记录集合：users/*/history/*。
表示用户个人资料的资源：users/*/profile。
表示用户设置的资源：users/*/settings。
Cloud Pub/Sub API
pubsub.googleapis.com 服务实现了 Cloud Pub/Sub AP，后者定义以下资源模型：
```

API 服务：pubsub.googleapis.com

```
主题集合：projects/*/topics/*。
订阅集合：projects/*/subscriptions/*。
```

Cloud Spanner API
spanner.googleapis.com 服务实现了 Cloud Spanner API，后者定义了以下资源模型：

API 服务：spanner.googleapis.com
- 实例集合：projects/\*/instances/\*。每个实例都具有以下资源。
- 操作的集合：projects/\*/instances/\*/operations/*。
- 数据库的集合：projects/\*/instances/\*/databases/*。 每个数据库都有以下资源。
    - 操作的集合：projects/\*/instances/\*/databases/\*/operations/*。
    - 会话集合：projects/\*/instances/\*/databases/\*/sessions/*。


#### 命名规则

- API 中使用的名称应采用正确的**美式英语**。例如，使用美式英语的 license、color，而非英式英语的 licence、colour。
- 为了简化命名，可以使用已被广泛接受的简写形式或缩写。例如，API 优于 Application Programming Interface。
- 尽量使用直观、熟悉的术语。例如，如果描述移除（和销毁）一个资源，则删除优于擦除。
- 使用相同的名称或术语命名同样的概念，包括跨 API 共享的概念。
- 避免名称过载。使用不同的名称命名不同的概念。
- 避免在 API 的上下文以及范围更大的 Google API 生态系统中使用含糊不清、过于笼统的名称。这些名称可能导致对 API 概念的误解。相反，应选择能准确描述 API 概念的名称。这对定义一阶 API 元素（例如资源）的名称尤其重要。没有需避免名称的明确列表，因为每个名称都必须放在其他名称的上下文中进行评估。实例、信息和服务的名称都曾出现过这类问题。所选择的名称应清楚地描述 API 概念（例如：什么的实例？），并将其与其他相关概念区分开（例如：“alert”是指规则、信号还是通知？）。
- 仔细考虑使用的名称是否可能与常用编程语言中的关键字存在冲突。您可以使用这些名称，但在 API 审核期间可能会触发额外的审查。因此应明智而审慎地使用。


## REF
- [google api design](https://cloud.google.com/apis/design/resources?hl=zh-cn)
