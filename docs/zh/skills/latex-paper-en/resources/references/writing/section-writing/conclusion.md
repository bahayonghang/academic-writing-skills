# 结论部分写作

## 客观的

通过用有限的证据、影响、局限性和具体的未来方向回答引言中的承诺来结束本文。

## 所需角色

1. **已解决的问题**：重申目标问题和核心技术思想。
2. **证据回顾**：总结最有支持的发现并设定界限。
3. **含义**：说明结果能够实现或建议什么。
4. **限制**：在不破坏整个贡献的情况下指定一个真实的范围边界。
5. **未来的工作**：将限制与具体的下一个方向联系起来。

## 关闭检查

地图简介承诺结论答案：

```text
Intro claim: ...
Conclusion answer: ...
Evidence anchor: ...
Status: closed / weakly closed / missing
```

如果承诺没有得到答复，只有在证据存在的情况下才添加有限制的答案。否则标记缺失的证据。

## 限制指导

更喜欢范围限制而不是可避免的实施借口：

- 数据体系、领域或场景边界；
- 假设边界；
- 部署或传感器/设置边界；
- 规模或资源边界。

避免普遍的未来工作声明，例如“我们将提高性能”，除非当前的限制是特定的。

## 安全措辞

- `The presented results indicate ... in the evaluated setting`
- `A current limitation is ...`
- `Extending the method to ... remains an important direction`

避免：

- 当仅测试基准子集时为 `This solves ...`。
- `The method is universally applicable ...` 无跨域证据。
