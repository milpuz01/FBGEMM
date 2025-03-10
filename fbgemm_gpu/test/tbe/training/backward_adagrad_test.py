#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

# pyre-ignore-all-errors[56]

import unittest
from typing import Any, Dict

from hypothesis import given, settings

from .backward_adagrad_common import (
    additional_decorators,
    adjust_mixed_B_st,
    BackwardAdagradTestCommon,
    common_settings,
    common_strategy,
    gpu_unavailable,
    optests,
    PoolingMode,
    SparseType,
    st,
)

# Set up test strategy
test_st: Dict[str, Any] = common_strategy.copy()
test_st["D"] = st.integers(min_value=2, max_value=128)


@optests.generate_opcheck_tests(fast=True, additional_decorators=additional_decorators)
class BackwardAdagradTest(BackwardAdagradTestCommon):
    @unittest.skipIf(*gpu_unavailable)
    @given(mixed_B=st.booleans(), **test_st)
    @settings(**common_settings)
    def test_backward_adagrad_fp16_pmSUM(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        kwargs = adjust_mixed_B_st(kwargs)
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP16,
            pooling_mode=PoolingMode.SUM,
            compile=False,  # FIXME: make compilation work for fp16
            **kwargs,
        )

    @unittest.skipIf(*gpu_unavailable)
    @given(
        mixed_B=st.booleans(),
        compile=st.booleans(),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp16_pmMEAN(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        kwargs = adjust_mixed_B_st(kwargs)
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP16,
            pooling_mode=PoolingMode.MEAN,
            **kwargs,
        )

    @unittest.skipIf(*gpu_unavailable)
    @given(
        compile=st.booleans(),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp16_pmNONE(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP16,
            pooling_mode=PoolingMode.NONE,
            mixed_B=False,
            **kwargs,
        )

    @given(
        mixed_B=st.booleans(),
        compile=st.booleans(),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp32_pmSUM(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        kwargs = adjust_mixed_B_st(kwargs)
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP32,
            pooling_mode=PoolingMode.SUM,
            **kwargs,
        )

    @given(
        mixed_B=st.booleans(),
        compile=st.booleans(),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp32_pmMEAN(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        kwargs = adjust_mixed_B_st(kwargs)
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP32,
            pooling_mode=PoolingMode.MEAN,
            **kwargs,
        )

    @unittest.skipIf(*gpu_unavailable)
    @given(
        compile=st.booleans(),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp32_pmNONE(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP32,
            mixed_B=False,
            pooling_mode=PoolingMode.NONE,
            **kwargs,
        )

    @unittest.skipIf(*gpu_unavailable)
    @given(
        mixed_B=st.booleans(),
        max_norm=st.floats(min_value=0.01, max_value=1.0),
        **test_st,
    )
    @settings(**common_settings)
    def test_backward_adagrad_fp16_pmSUM_with_max_norm(  # noqa C901
        self,
        **kwargs: Any,
    ) -> None:
        kwargs = adjust_mixed_B_st(kwargs)
        fixed_strategy = {"row_wise": True, "use_cpu": False}
        for key, val in fixed_strategy.items():
            assert key in kwargs
            kwargs[key] = val
        self.execute_backward_adagrad(
            weights_precision=SparseType.FP16,
            pooling_mode=PoolingMode.SUM,
            **kwargs,
        )


if __name__ == "__main__":
    unittest.main()
