const broker = {
  host: '127.0.0.1:7890',
  basePath: '/hermes/v1/secret',
  enabled: true,
};

const brokerFetchAction = async (operation, payload = {}) => {
  if (!broker.enabled) throw new Error('broker disabled');
  const url = `http://${broker.host}${broker.basePath}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ operation, ...payload }),
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(`broker http ${res.status}`);
  return res.json();
};

const api = {
  add: (item) => brokerFetchAction('add', item),
  update: (item) => brokerFetchAction('update', item),
  remove: (key) => brokerFetchAction('remove', { key }),
  list: (kind) => {
    const qs = kind ? `?kind=${encodeURIComponent(kind)}` : '';
    return fetch(`http://${broker.host}${broker.basePath}/list${qs}`, { cache: 'no-store' }).then(r => r.json());
  },
  fetch: () => fetch(`http://${broker.host}${broker.basePath}/fetch`, { cache: 'no-store' }).then(r => r.json()),
  import_json: (file) => brokerFetchAction('import_json', { path: file }),
  export_env: (path) => brokerFetchAction('export_env', { path }),
  clear: () => brokerFetchAction('clear', { confirm: 'yes' }),
};
