// Based on https://github.com/graphql/graphiql/blob/HEAD/packages/graphiql-plugin-explorer/examples/index.html


// const evtSource = new EventSource("/graphql-sse-test");


// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of
class AsyncQueue {
  constructor() {
    this.queue = [];   // Items pushed to the queue
    this.waiting = []; // Waiting pulls from consummers
  }

  push(item) {
    // If consummers are waiting, immediately send the item
    if (this.waiting.length > 0) {
      const deferred = this.waiting.shift();
      deferred.resolve({ value: item, done: false });
    } else {
      // Otherwise, put it in the queue
      this.queue.push(item);
    }
  }
  next() {
    // Send the next item if we have one
    if (this.queue.length > 0) {
      const value = this.queue.shift();
      return Promise.resolve({ value, done: false });
    } else {
    // Defer the return if we don't have an item ready
      let deferred;
      const promise = new Promise((resolve, reject) => {
        deferred = { resolve, reject };
      });
      this.waiting.push(deferred);
      return promise;
    }
  }

  [Symbol.asyncIterator]() {
    return {
      next: () => {
        return this.next();
      },

      return: () => {
        // Clean up any pending promises
        this.waiting.forEach(d => d.resolve({ done: true }));
        this.waiting = [];
        return Promise.resolve({ done: true });
      }
    };
  }
}


function makeGraphiQLFetcher(fetcherOptions) {
  const graphqlUrl = fetcherOptions.graphqlUrl;
  const graphqlSSEUrl = fetcherOptions.graphqlSSEUrl;

  const fetcher = (payload, opts) => {
    let dumped_payload = JSON.stringify(payload);

    let isSubscription = payload.query.trim().startsWith("subscription");
    if (!isSubscription) {
      // https://graphiql-test.netlify.app/typedoc/modules/graphiql_react.html
      // https://github.com/graphql/graphiql/blob/main/packages/graphiql-toolkit/docs/create-fetcher.md
      return fetch(graphqlUrl, {
          method: 'post',
          body: dumped_payload,
      }).then(response => response.json());
    }

    let sse_url = `${graphqlSSEUrl}?query=${btoa(dumped_payload)}`

    let throwMe = null;
    const queue = new AsyncQueue();

    // https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
    const evtSource = new EventSource(sse_url);
    evtSource.onmessage = (event) => {
        queue.push(JSON.parse(event.data))
    };
    evtSource.onerror = (error) => {
      throwMe = error;
    }
    
    return {
      [Symbol.asyncIterator]() {
        return this;
      },
      async next() {
        if (throwMe) throw throwMe;
        return queue.next();
      },
      async return() {
        return { done: true, value: undefined };
      },
    };
  }
  return fetcher;
}


var graphQLFetcher = makeGraphiQLFetcher({
  graphqlUrl: '/graphql',
  graphqlSSEUrl: '/graphql-sse',
})
function GraphiQLWithExplorer() {
    var [query, setQuery] = React.useState(
      '',
    );
    var explorerPlugin = GraphiQLPluginExplorer.useExplorerPlugin({
      query: query,
      onEdit: setQuery,
    });
    return React.createElement(GraphiQL, {
      fetcher: graphQLFetcher,
      defaultEditorToolsVisibility: true,
      plugins: [explorerPlugin],
      query: query,
      onEditQuery: setQuery,
    });
  }
ReactDOM.render(
    React.createElement(GraphiQLWithExplorer),
    document.getElementById('graphiql')
);
