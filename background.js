let color = '#3aa757';

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({ color });
  console.log('Default background color set to %cgreen', `color: ${color}`);
});


chrome.notifications.create(
  "2131231",
  {
    type: "basic",
    iconUrl: "/images/get_started16.png",
    title: "喝水小助手",
    message: "看到此消息的人可以和我一起来喝一杯水",
  },
  () => {
    console.log('notificatoins done');
  }
);