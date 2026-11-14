(() => {
  document.querySelectorAll('[data-trace]').forEach(button=>button.addEventListener('click',()=>{
    const value=button.dataset.trace, seconds={eeg:2,ppg:6,fnirs:30}[value];
    document.querySelectorAll('[data-trace]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    document.querySelectorAll('[data-wave]').forEach(path=>{path.style.display=path.dataset.wave===value?'':'none';});
    document.querySelectorAll('[data-trace-note]').forEach(n=>{n.hidden=n.dataset.traceNote!==value;});
    document.querySelector('#trace-mid').textContent=`${seconds/2} s`;
    document.querySelector('#trace-end').textContent=`${seconds} s`;
  }));
})();
