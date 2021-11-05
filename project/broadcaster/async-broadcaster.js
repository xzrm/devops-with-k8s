// const lo = require('lodash')
const { connect, JSONCodec } = require("nats");
const { get } = require("axios");

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const CHAT_ID = process.env.CHAT_ID;


async function sendMessage(message) {
  const markdownFormatString = `\`\`\`json ${JSON.stringify(message)}\`\`\``;
  const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage?chat_id=${CHAT_ID}&parse_mode=Markdown&text=${markdownFormatString}`;
  const response = await get(url);
}


// Create a connection to NATS server
const start = async function () {
  console.log("Started listening...")
  const nc = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });

  // create a codec
  const jc = JSONCodec();
  const sub = nc.subscribe("updates");
  (async () => {
    for await (const m of sub) {
      console.log("received message")
      const payload = jc.decode(m.data)
      await sendMessage(payload);
    }
  })();
}
start();

