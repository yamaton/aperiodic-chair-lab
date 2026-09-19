/* Presentation of exact contact results; never decides geometric validity. */
(function (root) {
  'use strict';
  const styles = {
    good: {
      className: '', label: '適合', detail: '適合',
      dashed: false, priority: 0,
    },
    arrow: {
      className: 'arrow-mismatch', label: '矢印違い', detail: '矢印の向きが違います',
      dashed: true, priority: 1,
    },
    symbol: {
      className: 'symbol-mismatch', label: '模様違い', detail: '模様が違います',
      dashed: false, priority: 1,
    },
  };

  function describe(contact) {
    return contact.ok ? styles.good : contact.patterns ? styles.arrow : styles.symbol;
  }

  // A locally matching face may still belong to an overlapping/invalid placement.
  function status(result) {
    if (result.ok) return 'good';
    const arrowsOnly = !result.overlap.length &&
      result.contacts.some(c => describe(c) === styles.arrow) &&
      result.contacts.every(c => c.patterns);
    return arrowsOnly ? 'arrow-mismatch' : 'bad';
  }

  const api = {describe, status};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ChairFeedback = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
