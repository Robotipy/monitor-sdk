/**
 * BotMonitor — Node.js SDK.
 *
 * Usage:
 *   const { BotMonitor } = require("@robotipy/botmonitor");
 *   const monitor = new BotMonitor({ url, apiKey, botId });
 *   await monitor.ping();
 */

const { randomUUID } = require("crypto");

class BotMonitor {
    #url;
    #apiKey;
    #botId;
    #headers;
    #currentJobId = null;
    #currentJobStart = null;

    constructor({ url, apiKey, botId } = {}) {
        this.#url = (url || process.env.BOTMONITOR_URL || "{{API_URL}}").replace(/\/+$/, "");
        this.#apiKey = apiKey || process.env.BOTMONITOR_API_KEY || "{{API_KEY}}";
        this.#botId = botId || process.env.BOTMONITOR_BOT_ID || "{{BOT_ID}}";
        this.#headers = {
            "Content-Type": "application/json",
            "x-api-key": this.#apiKey,
            "x-bot-id": this.#botId,
        };
    }

    async #post(path, body) {
        try {
            const res = await fetch(`${this.#url}${path}`, {
                method: "POST",
                headers: this.#headers,
                body: JSON.stringify(body),
                signal: AbortSignal.timeout(5000),
            });
            return await res.json();
        } catch (err) {
            console.error(`[BotMonitor] ${path} failed:`, err.message);
            return null;
        }
    }

    async ping(message = "alive", level = "INFO", meta) {
        const body = { level, message, type: "ping" };
        if (meta) body.meta = meta;
        return this.#post("/api/logs", body);
    }

    async startJob(jobName, jobId, meta) {
        this.#currentJobId = jobId || randomUUID();
        this.#currentJobStart = Date.now();

        const body = {
            level: "INFO",
            message: `Job started: ${jobName || this.#currentJobId}`,
            type: "start",
            job_id: this.#currentJobId,
        };
        if (jobName) body.job_name = jobName;
        if (meta) body.meta = meta;

        await this.#post("/api/logs", body);
        return this.#currentJobId;
    }

    async endJob(jobId, status = "ok", meta) {
        const jid = jobId || this.#currentJobId;
        if (!jid) {
            console.error("[BotMonitor] endJob called without a job_id");
            return;
        }

        let elapsed = "";
        if (this.#currentJobStart) {
            elapsed = ` (${((Date.now() - this.#currentJobStart) / 1000).toFixed(1)}s)`;
        }

        const body = {
            level: status === "error" ? "ERROR" : "INFO",
            message: `Job ended: ${jid}${elapsed}`,
            type: "end",
            job_id: jid,
            status,
        };
        if (meta) body.meta = meta;

        const result = await this.#post("/api/logs", body);

        if (jid === this.#currentJobId) {
            this.#currentJobId = null;
            this.#currentJobStart = null;
        }

        return result;
    }

    async log(message, level = "INFO", meta) {
        const body = { level, message };
        if (meta) body.meta = meta;
        return this.#post("/api/logs", body);
    }
}

module.exports = { BotMonitor };
