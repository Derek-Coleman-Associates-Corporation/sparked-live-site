/* No API calls, analytics payloads or browser storage. Visitors send in WhatsApp. */
document.querySelectorAll('[data-interest-form]').forEach(function (form) {
  var review = form.querySelector('[data-review]');
  var draft = form.querySelector('[data-draft]');
  var link = form.querySelector('[data-whatsapp-link]');
  var role = form.querySelector('[name="role"]');
  var handle = form.querySelector('[name="handle"]');
  function resetReview() {
    review.hidden = true;
    link.removeAttribute('href');
  }
  form.addEventListener('input', resetReview);
  form.addEventListener('change', function () {
    handle.required = role.value === 'creator';
    resetReview();
  });
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;
    var lines = [form.dataset.message];
    form.querySelectorAll('[data-message-label]').forEach(function (field) {
      var value = field.value.trim();
      if (!value) return;
      if (field.tagName === 'SELECT') value = field.selectedOptions[0].textContent;
      lines.push(field.dataset.messageLabel + ': ' + value);
    });
    draft.value = lines.join('\n');
    link.href = 'https://wa.me/' + form.dataset.whatsapp + '?text=' + encodeURIComponent(draft.value);
    review.hidden = false;
    draft.focus();
  });
  form.querySelector('[data-prepare]').disabled = false;
});
