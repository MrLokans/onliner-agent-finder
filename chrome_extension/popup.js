// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  renderStatus('Extension is working.');
  var elements = document.querySelectorAll('apartment-info__sub-line_extended');
});
